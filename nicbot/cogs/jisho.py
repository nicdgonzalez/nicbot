from __future__ import annotations

import logging
from typing import TYPE_CHECKING, cast

from discord.ext import commands
from jisho_api.kanji import Kanji
from jisho_api.sentence import Sentence
from jisho_api.word import Word

from ..bot import NicBot
from ..utils import auto_add_cogs

if TYPE_CHECKING:
    type Context = commands.Context[NicBot]

_log = logging.getLogger(__name__)


class Jisho(commands.Cog):
    """Search sentences and definitions from a Japanese dictionary."""

    def __init__(self, bot: commands.Bot, /) -> None:
        self.bot = cast(NicBot, bot)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        _log.info(f"Loaded cog {self.__class__.__name__!r}")

    @commands.group()
    async def jisho(self, ctx: Context, /) -> None:
        return

    # TODO: If query has more than one kanji, search each kanji individually
    # and return the results in a pager.
    # TODO: If query is not a kanji, try to convert it into Kanji for the user.
    # (e.g., try to convert とり into 鳥)
    @jisho.command()
    async def kanji(self, ctx: Context, /, query: str) -> None:
        """Look for a kanji's definition in the Japanese dictionary."""
        response = Kanji.request(query)

        if response is None:
            await ctx.reply("No results found. Did you submit kanji?")
            return

        entry = response.data

        kanji = entry.kanji
        strokes = entry.strokes
        main_meanings = ", ".join(entry.main_meanings)
        readings_kun = ", ".join(entry.main_readings.kun)
        readings_on = ", ".join(entry.main_readings.on)

        message = (
            f"**Kanji**: {kanji}\n"
            f"**Strokes**: {strokes}\n"
            f"**Main Meanings**: {main_meanings}\n"
            f"**Kun'yomi**: {readings_kun}\n"
            f"**On'yomi**: {readings_on}\n"
        )

        await ctx.reply(message)

    # TODO: Create a pager for the results.
    # TODO: If a query has 2 or more words in it, try to split the result
    # by replacing the previously matched entry with an empty string and repeat
    # until the original query is empty. I feel like this might return
    # too many results, so maybe not...
    @jisho.command()
    async def word(self, ctx: Context, /, query: str) -> None:
        """Look up a word in the Japanese dictionary."""
        response = Word.request(query)

        if response is None:
            await ctx.reply("No results found. Are you making up words? >.>")
            return

        data = response.data

        # Each result that is returned will receive its own page.
        page = 0

        # The total number of results returned by the query.
        # total_pages = len(data)

        entry = data[page]
        assert len(entry.japanese) >= 1, entry.japanese
        _log.debug(entry)
        word = entry.japanese[0].word
        reading = entry.japanese[0].reading
        jlpt = ", ".join([e.replace("jlpt-", "").upper() for e in entry.jlpt])
        assert len(entry.senses) >= 1, entry.senses
        parts_of_speech = ", ".join(entry.senses[0].parts_of_speech)
        english_definitions = ", ".join(entry.senses[0].english_definitions)
        antonyms = ", ".join(entry.senses[0].antonyms)

        message = (
            f"**Word**: {word}\n"
            f"**Reading**: {reading}\n"
            f"**JLPT**: {jlpt}\n"
            f"**Parts of Speech**: {parts_of_speech}\n"
            f"**English Defintions**: {english_definitions}\n"
            f"**Antonyms**: {antonyms}\n"
        )

        await ctx.reply(message)

    # TODO: Finish implementing this...
    @jisho.command()
    async def sentence(self, ctx: Context, /, query: str) -> None:
        """Look up a sentence in the Japanese dictionary."""
        response = Sentence.request(query)
        print("Response:", response)
        print(type(response))
        print("Data:", response.data)
        print(type(response.data))


# Required at the end of all extension modules.
async def setup(bot: commands.Bot, /) -> None:
    await auto_add_cogs(bot)
