from __future__ import annotations

import datetime as dt
import logging
import pathlib
import argparse
import os
from typing import TYPE_CHECKING

from .bot import NicBot

try:
    import dotenv
except ImportError:
    pass  # Skip loading the .env file.
else:
    _ = dotenv.load_dotenv()

if TYPE_CHECKING:
    LoggingLevel = type(logging.DEBUG)

# Authorizes the bot to use the Discord API:
# https://discord.com/developers/docs/reference#authentication
if (DISCORD_TOKEN := os.getenv("DISCORD_TOKEN")) is None:
    raise KeyError("expected environment variable DISCORD_TOKEN to be defined")


def main() -> None:
    """The main entry point to the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        help="Logger emits more verbose messages",
        action="count",  # You can stack the flag (e.g., -v == 1, -vv == 2)
    )
    args = parser.parse_args()

    if args.verbose == 0:
        level = logging.WARNING
    elif args.verbose == 1:
        level = logging.INFO
    else:
        level = logging.DEBUG

    start_logger(level)

    bot = NicBot()
    bot.run(DISCORD_TOKEN)


def start_logger(level: LoggingLevel) -> None:
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 format
    )

    # The logs directory lives at the same level as the current directory.
    logs_dirpath = pathlib.Path(__file__).parents[1].joinpath("logs")

    if not logs_dirpath.exists():
        logs_dirpath.mkdir()

    today = dt.datetime.now()
    log_filepath = logs_dirpath.joinpath(today.strftime("%Y-%m-%d.log"))

    file_handler = logging.FileHandler(log_filepath, mode="a")
    file_handler.setFormatter(formatter)

    logging.root.addHandler(file_handler)
    logging.root.setLevel(level)


if __name__ == "__main__":
    main()
