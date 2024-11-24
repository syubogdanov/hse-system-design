from argparse import ArgumentParser

from src.presentation.http.launcher import HttpApiLauncher


def get_parser() -> ArgumentParser:
    """Получить интерфейс командной строки."""
    parser = ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--start-http-api", action="store_true")

    return parser


def main() -> None:
    """Запустить компоненту."""
    parser = get_parser()
    args = parser.parse_args()

    if args.start_http_api:
        HttpApiLauncher.launch()


if __name__ == "__main__":
    main()
