from __future__ import annotations

import argparse
import logging
import os
from typing import TYPE_CHECKING

from .bot import NicBot
from .logger import start_logging

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

    start_logging(level)

    bot = NicBot()
    bot.run(DISCORD_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
