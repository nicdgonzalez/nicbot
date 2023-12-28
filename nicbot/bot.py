import logging
import os
import pathlib

import discord
from discord.ext import commands
from overrides import override

_log = logging.getLogger(__name__)


class NicBot(commands.Bot):
    """A bot that runs on Discord."""

    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            case_insensitive=True,
            description="A bot that runs on Discord.",
            self_bot=False,
            owner_id=None,
            strip_after_prefix=True,
            intents=discord.Intents.all(),
        )

    @override
    async def setup_hook(self) -> None:
        cogs = pathlib.Path(__file__).parent.joinpath("cogs")

        # Automatically discover and load extensions onto the bot instance.
        for extension in os.listdir(cogs):
            if extension.startswith("_"):
                continue

            if not extension.endswith(".py"):
                continue

            name = "." + extension.removesuffix(".py")

            try:
                await self.load_extension(name, package="nicbot.cogs")
            except Exception as exc:
                _log.error(f"Failed to load extension {name!r}: {exc}")

    async def on_ready(self) -> None:
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name="Happy Holidays! 🎄",
        )

        await self.change_presence(
            activity=activity, status=discord.Status.online
        )

        assert self.user is not None
        _log.info(f"Logged in as {self.user.name!r}")
