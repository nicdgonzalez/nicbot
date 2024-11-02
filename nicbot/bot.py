import logging
import os
import pathlib
import tomllib
from typing import Any

import discord
import overrides
from discord.ext import commands

_log = logging.getLogger(__name__)


def loadable_cog_extension(filename: str) -> bool:
    return filename.endswith(".py") and not filename.startswith("_")


def get_pyproject_config() -> dict[str, Any]:
    """Reads the project's `pyproject.toml` and returns the configuration."""
    root = pathlib.Path(__file__).parents[1]
    pyproject_toml = root.joinpath("pyproject.toml")
    assert pyproject_toml.exists()

    with open(pyproject_toml, "rb") as f:
        config = tomllib.load(f)

    return config


class NicBot(commands.Bot):
    """Represents a bot that runs on Discord"""

    def __init__(self) -> None:
        config = get_pyproject_config()
        assert "project" in config.keys(), config.keys()

        project_config: dict[str, Any] = config.get("project")
        assert "description" in project_config.keys(), project_config.keys()

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            case_insensitive=True,
            description=project_config.get("description", ""),
            self_bot=False,
            # Let the library automatically resolve the owner(s).
            owner_id=None,
            owner_ids=None,
            strip_after_prefix=True,
            intents=discord.Intents.all(),
        )

    @overrides.override
    async def setup_hook(self) -> None:
        cogs = pathlib.Path(__file__).parent.joinpath("cogs")

        # Automatically discover and load extensions onto the bot instance.
        files = os.listdir(cogs)
        extensions = filter(loadable_cog_extension, files)

        for extension in extensions:
            name = "." + extension.removesuffix(".py")

            try:
                await self.load_extension(name, package="nicbot.cogs")
            except Exception as exc:
                _log.error(f"unable to load extension {name!r}: {exc}")

    async def on_ready(self) -> None:
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="僕のヒーローアカデミア",
        )

        assert isinstance(activity, discord.Activity)
        await self.change_presence(
            activity=activity, status=discord.Status.online
        )

        assert self.user is not None
        _log.info(f"Logged in as {self.user.name!r}")
