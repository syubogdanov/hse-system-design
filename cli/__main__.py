from argparse import ArgumentParser

from src.presentation.crontab.launcher import CrontabLauncher
from src.presentation.grpc.launcher import GrpcApiLauncher
from src.presentation.http.launcher import HttpApiLauncher
from src.presentation.migrations.launcher import MigrationsLauncher
from src.presentation.stream.launcher import StreamLauncher


def get_parser() -> ArgumentParser:
    """Получить интерфейс командной строки."""
    parser = ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start-http-api", action="store_true")
    group.add_argument("--start-crontab", action="store_true")
    group.add_argument("--start-stream", action="store_true")
    group.add_argument("--start-grpc-api", action="store_true")
    group.add_argument("--start-migrations", action="store_true")

    return parser


def main() -> None:
    """Запустить компоненту."""
    parser = get_parser()
    args = parser.parse_args()

    if args.start_http_api:
        HttpApiLauncher.launch()

    if args.start_crontab:
        CrontabLauncher.launch()

    if args.start_stream:
        StreamLauncher.launch()

    if args.start_grpc_api:
        GrpcApiLauncher.launch()

    if args.start_migrations:
        MigrationsLauncher.launch()


if __name__ == "__main__":
    main()
