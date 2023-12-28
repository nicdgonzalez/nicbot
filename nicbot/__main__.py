from __future__ import annotations

import logging
import os
import pathlib
import sys
from typing import TYPE_CHECKING

from .bot import NicBot

if TYPE_CHECKING:
    from builtins import list as List

_log = logging.getLogger(__name__)


def logging_setup() -> None:
    """Configure logging for the program."""
    handlers: List[logging.Handler] = []
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S%z",
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    handlers.append(stream_handler)

    # Add additional handlers (e.g. file handler).
    ...

    for handler in handlers:
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)

    logging.root.setLevel(logging.INFO)


def main() -> int:
    """The main entry-point to the program.

    Returns
    -------
    :class:`int`
        The exit code of the program.
    """
    env_file = pathlib.Path(__file__).parents[1].joinpath(".env")
    logging_setup()

    try:
        import dotenv
    except ImportError:
        _log.warning("(Skipping) Failed to load package 'python-dotenv'.")
    else:
        dotenv.load_dotenv(env_file)

    bot = NicBot()
    bot.run(os.environ["DISCORD_TOKEN"])

    return 0


if __name__ == "__main__":
    sys.exit(main())
