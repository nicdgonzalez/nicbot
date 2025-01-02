from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

from discord.ext import commands

from ..bot import NicBot
from ..utils import auto_add_cogs

if TYPE_CHECKING:
    ...

_log = logging.getLogger(__name__)


class Moderator(commands.Cog):
    def __init__(self, bot: commands.Bot, /) -> None:
        self.bot = cast(NicBot, bot)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        _log.info(f"Loaded cog {self.__class__.__name__!r}")

    @commands.is_owner()
    @commands.command()
    async def unload(self, ctx: commands.Context[NicBot], name: str) -> None:
        await self.bot.unload_extension(name=f".{name}", package="nicbot.cogs")
        await ctx.reply(f"Successfully unloaded extension {name!r}")

    @commands.is_owner()
    @commands.command()
    async def load(self, ctx: commands.Context[NicBot], name: str) -> None:
        await self.bot.load_extension(name=f".{name}", package="nicbot.cogs")
        await ctx.reply(f"Successfully loaded extension {name!r}")

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx: commands.Context[NicBot], name: str) -> None:
        name_raw = name
        name = f".{name}"

        await self.bot.unload_extension(name=name, package="nicbot.cogs")
        await self.bot.load_extension(name=name, package="nicbot.cogs")
        await ctx.reply(f"Successfully reloaded extension {name_raw!r}")


# Required at the end of all extension modules.
async def setup(bot: commands.Bot, /) -> None:
    await auto_add_cogs(bot)
