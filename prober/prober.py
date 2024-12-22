import sys
import logging
from dataclasses import dataclass, asdict
from random import random

import requests
import signal
import time
import uuid

from urllib3 import Retry

from environs import Env
from prometheus_client import start_http_server, Gauge, Counter

CANCELLATION_PERCENTAGE = 0.05

PROBER_CREATE_ORDERS_TOTAL = Counter(
    "prober_create_orders_total",
    "Total counts of runs the create scenario of order to sorting hat API",
)

PROBER_CREATE_ORDERS_SUCCESS_TOTAL = Counter(
    "prober_create_orders_success_total",
    "Total counts of success runs the create scenario of order to sorting hat API",
)

PROBER_CREATE_ORDERS_FAIL_TOTAL = Counter(
    "prober_create_orders_fail_total",
    "Total counts of fail runs the create scenario of order to sorting hat API",
)

PROBER_CREATE_ORDERS_DURATION_SECONDS = Gauge(
    "prober_create_orders_duration_seconds",
    "Duration in seconds of runs the create scenario of order to sorting hat API",
)

PROBER_CANCEL_ORDERS_TOTAL = Counter(
    "prober_cancel_orders_total",
    "Total counts of runs the cancel scenario of order to sorting hat API",
)

PROBER_CANCEL_ORDERS_SUCCESS_TOTAL = Counter(
    "prober_cancel_orders_success_total",
    "Total counts of success runs the cancel scenario of order to sorting hat API",
)

PROBER_CANCEL_ORDERS_FAIL_TOTAL = Counter(
    "prober_cancel_orders_fail_total",
    "Total counts of fail runs the cancel scenario of order to sorting hat API",
)

env = Env()
env.read_env()

session = requests.Session()
retry = Retry(connect=3, backoff_factor=1)
session.mount("http://", requests.adapters.HTTPAdapter(max_retries=retry))


class Config(object):
    sorting_hat_exporter_api_url = env("API_URL", "")
    sorting_hat_scrape_interval = env.float("SCRAPE_INTERVAL", 1)
    sorting_hat_log_level = env.log_level("LOG_LEVEL", logging.INFO)
    sorting_hat_exporter_metrics_port = env.int("METRICS_PORT", 6200)


@dataclass
class OrderItem:
    id: str
    source_address_id: str
    target_address_id: str


class ProberClient:
    def __init__(self, config: Config) -> None:
        self.api_url = config.sorting_hat_exporter_api_url

    def probe(self) -> None:
        PROBER_CREATE_ORDERS_TOTAL.inc()
        logging.info("Try create new order")
        new_order = OrderItem(
            id=str(uuid.uuid4()),
            source_address_id=str(uuid.uuid4()),
            target_address_id=str(uuid.uuid4()),
        )

        start = time.perf_counter()
        try:
            create_request = session.post("{}/api/v1/orders/register".format(self.api_url),
                                          json=asdict(new_order))
            if create_request and create_request.status_code == 202:
                PROBER_CREATE_ORDERS_SUCCESS_TOTAL.inc()
            else:
                PROBER_CREATE_ORDERS_FAIL_TOTAL.inc()
        except Exception as err:
            logging.error(err)
            PROBER_CREATE_ORDERS_FAIL_TOTAL.inc()

        duration = time.perf_counter() - start
        PROBER_CREATE_ORDERS_DURATION_SECONDS.set(duration)

        if random() < CANCELLATION_PERCENTAGE:
            try:
                delete_request = session.delete("{}/api/v1/orders/{}/pipelines/latest/cancel".
                                                format(self.api_url, new_order.id))
                if delete_request and delete_request.status_code == 200:
                    PROBER_CANCEL_ORDERS_SUCCESS_TOTAL.inc()
                else:
                    PROBER_CANCEL_ORDERS_FAIL_TOTAL.inc()
            except Exception as err:
                logging.error(err)
                PROBER_CANCEL_ORDERS_FAIL_TOTAL.inc()


def setup_logging(config: Config) -> None:
    logging.basicConfig(
        stream=sys.stdout,
        level=config.sorting_hat_log_level,
        format="%(asctime)s %(levelname)s:%(message)s",
    )


def main() -> None:
    config = Config()
    setup_logging(config)

    logging.info("Starting prober exporter on port: {}".format(config.sorting_hat_exporter_metrics_port))
    start_http_server(config.sorting_hat_exporter_metrics_port)
    client = ProberClient(config)

    while True:
        logging.info("Run prober")
        client.probe()

        logging.info("Waiting {} seconds for next loop".format(config.sorting_hat_scrape_interval))
        time.sleep(config.sorting_hat_scrape_interval)


def terminate(signal, frame) -> None:
    print("Terminating")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, terminate)
    main()
