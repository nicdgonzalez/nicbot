from __future__ import annotations

import inspect
import sys
from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from builtins import type as Type
    from typing import Iterable, Optional


async def auto_add_cogs(
    bot: commands.Bot,
    *,
    name: Optional[str] = None,
    ignore: Iterable[Type[commands.Cog]] = tuple(),
) -> None:
    """Automatically discover all of the classes in a module that subclass
    :class:`discord.ext.command.Cog` and add the cog to the bot instance.

    .. warning::

        This function relies on inspecting the caller's stack information,
        which makes it very fragile. See Examples for intended usage.

    Parameters
    ----------
    bot: :class:`discord.ext.commands.Bot`
        An instance of a bot to add the cogs to.

    Other Parameters
    ----------------
    name: Optional[:class:`str`]
        This is normally resolved automatically using a modules ``__name__``
        attribute. If necessary, you can pass the attribute manually.
    ignore: Iterable, optional
        An iterable of class objects to skip when adding cogs to the bot.

    Examples
    --------
    >>> from discord.ext import commands
    >>>
    >>> from .. import utils
    >>>
    >>>
    >>> class MyCog(commands.Cog):
    ...     def __init__(self, bot: commands.Bot) -> None:
    ...         self.bot = bot
    ...
    ...     # define commands/events
    >>>
    >>>
    >>> # Required at the end of all extension modules
    >>> async def setup(bot: commands.Bot, /) -> None:
    ...     await utils.auto_add_cogs(bot)
    """
    if name is None:
        caller = inspect.stack()[1]
        module = inspect.getmodule(caller.frame)

        if module is None:
            raise ValueError("Failed to resolve module automatically.")

        name = module.__name__

    for _, cog_type in inspect.getmembers(sys.modules[name], inspect.isclass):
        if not issubclass(cog_type, commands.Cog):
            continue

        if cog_type in ignore:
            continue

        await bot.add_cog(cog_type(bot))
