from typing import Final

from aiokafka.errors import KafkaError
from httpx import ConnectError, ConnectTimeout
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed


WAIT: Final[float] = 1.0
ATTEMPTS: Final[int] = 5


retry_database = retry(
    reraise=True,
    retry=retry_if_exception_type((TimeoutError, OSError)),
    stop=stop_after_attempt(ATTEMPTS),
    wait=wait_fixed(WAIT),
)

retry_external_api = retry(
    reraise=True,
    retry=retry_if_exception_type((ConnectError, ConnectTimeout, OSError)),
    stop=stop_after_attempt(ATTEMPTS),
    wait=wait_fixed(WAIT),
)

retry_kafka = retry(
    reraise=True,
    retry=retry_if_exception_type((KafkaError, TimeoutError, OSError)),
    stop=stop_after_attempt(ATTEMPTS),
    wait=wait_fixed(WAIT),
)
