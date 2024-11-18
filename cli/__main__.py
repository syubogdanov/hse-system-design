from argparse import ArgumentParser

from dotenv import load_dotenv

from src.container import CONTAINER
from src.presentation.crontab.launcher import CrontabLauncher
from src.presentation.stream.launcher import StreamLauncher


def get_parser() -> ArgumentParser:
    """Получить интерфейс командной строки."""
    parser = ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start-api", action="store_true")
    group.add_argument("--start-crontab", action="store_true")
    group.add_argument("--start-stream", action="store_true")
    group.add_argument("--start-grpc", action="store_true")

    return parser


def main() -> None:
    """Запустить компоненту."""
    load_dotenv()

    parser = get_parser()
    args = parser.parse_args()

    logger = CONTAINER.logger()

    if args.start_api:
        logger.info("Starting the API...")
        raise NotImplementedError

    if args.start_crontab:
        logger.info("Starting the crontab...")
        CrontabLauncher.launch()

    if args.start_stream:
        logger.info("Starting the stream...")
        StreamLauncher.launch()

    if args.start_grpc:
        logger.info("Starting the gRPC...")
        raise NotImplementedError


if __name__ == "__main__":
    main()
