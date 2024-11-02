import inspect
import logging
import sys

from discord.ext import commands

__all__ = ("auto_add_cogs",)

_log = logging.getLogger(__name__)


async def auto_add_cogs(bot: commands.Bot, *, name: str = "") -> None:
    """Automatically discover which classes in a module subclass
    :class:`discord.ext.commands.Cog` and add them to the bot instance.

    .. warning::

        This function inspects the caller's stack information to get
        the module's `__name__` attribute, which makes it very fragile.
        See the Examples section for intended usage.

    Parameters
    ----------
    bot: :class:`discord.ext.commands.Bot`
        The bot instance to add the cog(s) to

    Other Parameters
    ----------------
    name: :class:`str`, optional
        The module's `__name__` attribute. This is normally resolved for you
        automatically, but if necessary, you can pass it manually here.

    Examples
    --------
    >>> from discord.ext import commands
    >>>
    >>> from ..utils import auto_add_cogs
    >>>
    >>>
    >>> class MyCog(commands.Cog):
    ...     def __init__(self, bot: commands.Bot) -> None:
    ...         self.bot = bot
    ...
    ...     # Define commands/events here...
    >>>
    >>>
    >>> # Required at the end of all extension modules.
    >>> async def setup(bot: commands.Bot, /) -> None:
    ...     await auto_add_cogs(bot)
    """
    if not name:
        caller = inspect.stack()[1]
        module = inspect.getmodule(caller.frame)

        if module is None:
            raise ValueError(
                "Failed to resolve module name automatically. Please use "
                "the 'name' parameter to pass the module's __name__ attribute "
                "manually (i.e., auto_add_cogs(bot, name=__name__)."
            )

        name = module.__name__
        _log.debug(f"Automatically resolved cog module name: {name}")

    # Returns the members of sys.modules[key] as ('name', <class Value>) pairs.
    members = inspect.getmembers(sys.modules[name], inspect.isclass)
    cogs = filter(lambda v: issubclass(v[1], commands.Cog), members)

    for _, cog_type in cogs:
        cog = cog_type(bot)
        await bot.add_cog(cog)
