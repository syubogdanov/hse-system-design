from argparse import ArgumentParser

from src.presentation.crontab.launcher import CrontabLauncher
from src.presentation.http.launcher import HttpApiLauncher
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
    parser = get_parser()
    args = parser.parse_args()

    if args.start_api:
        HttpApiLauncher.launch()

    if args.start_crontab:
        CrontabLauncher.launch()

    if args.start_stream:
        StreamLauncher.launch()

    if args.start_grpc:
        raise NotImplementedError


if __name__ == "__main__":
    main()
