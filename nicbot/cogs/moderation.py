from __future__ import annotations

import logging

from discord.ext import commands

from .. import utils

_log = logging.getLogger(__name__)


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        _log.info(f"Loaded Cog {self.__class__.__name__!r}")


async def setup(bot: commands.Bot, /) -> None:
    await utils.auto_add_cogs(bot)
