from __future__ import annotations

import json
import logging
import pathlib
import random
from typing import Literal, cast

import discord
from discord.ext import commands
from jisho_api.kanji import Kanji

from ..bot import NicBot
from ..utils import auto_add_cogs

_log = logging.getLogger(__name__)

file = pathlib.Path.cwd().resolve().joinpath("data", "kanji.json")
with open(file, "r") as f:
    KANJI = json.load(f)

JLPT_VALID_VALUES = tuple(KANJI.keys())


class KanjiOfTheDay(commands.Cog):
    """Command for sending the Kanji of the day to the Sunflower Field."""

    def __init__(self, bot: commands.Bot, /) -> None:
        self.bot = cast(NicBot, bot)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        _log.info(f"Loaded cog {self.__class__.__name__!r}")

    @commands.command()
    async def kotd(
        self,
        ctx: commands.Context[NicBot],
        /,
        kanji_or_jlpt: str = random.choice(JLPT_VALID_VALUES),
    ) -> None:
        jlpt: Literal["N1", "N2", "N3", "N4", "N5", "None"]

        kanji_or_jlpt = kanji_or_jlpt.upper()

        if kanji_or_jlpt in JLPT_VALID_VALUES:
            jlpt = kanji_or_jlpt
            kanji = random.choice(KANJI[jlpt])
        else:
            jlpt = "None"
            kanji = kanji_or_jlpt

        try:
            response = Kanji.request(kanji=kanji)
        except Exception:
            e = "error: failed to complete request"
            _log.error(e, exc_info=True)
            await ctx.reply(e)
            return

        entry = response.data

        # The entry's kanji is returned with a newline at the end.
        kanji = entry.kanji.strip()

        if jlpt == "None":
            if entry.meta.education.jlpt is not None:
                jlpt = entry.meta.education.jlpt
            else:
                for key, value in KANJI.items():
                    if kanji in value:
                        jlpt = key
                        break
                    else:
                        pass
                else:
                    jlpt = "None"

        kunyomi_reading = convert_readings_to_str(entry.main_readings.kun)
        onyomi_reading = convert_readings_to_str(entry.main_readings.on)
        main_meanings = ", ".join(entry.main_meanings)

        # Limit the number of examples to use.
        examples_kun = (
            entry.reading_examples.kun[0:3]
            if entry.reading_examples.kun is not None
            else []
        )
        examples_on = entry.reading_examples.on[0:3]

        def convert_to_vocabulary(e: object) -> str:
            return (
                f"- **{e.kanji}** ({e.reading}): {"; ".join(e.meanings[0:2])}"
            )

        vocabulary = list(map(convert_to_vocabulary, examples_kun))
        vocabulary += list(map(convert_to_vocabulary, examples_on))

        # The number of lines it takes to write this kanji.
        strokes = entry.strokes

        embed = discord.Embed(
            title=f"Kanji of the Day: {kanji}",
            description=(
                "Try writing the kanji yourself!\n"
                "And don't forget to share it with us ৻(  •̀ ᗜ •́  ৻)",
            ),
            color=0xBC002D,
        )
        embed.add_field(name="Meaning", value=main_meanings, inline=False)
        embed.add_field(name="Kun'yomi", value=kunyomi_reading, inline=True)
        embed.add_field(name="On'yomi", value=onyomi_reading, inline=True)
        embed.add_field(
            name="Vocabulary",
            value="\n".join(vocabulary),
            inline=False,
        )
        embed.add_field(name="JLPT", value=jlpt, inline=True)
        embed.add_field(name="Strokes", value=strokes, inline=True)

        filepath = get_kanji_stroke_order_filepath(kanji=kanji)

        with open(filepath, "rb") as f:
            file = discord.File(f, filename="kanji.png")

        embed.set_image(url="attachment://kanji.png")

        await ctx.reply(embed=embed, file=file)


def convert_readings_to_str(readings: list[str] | None) -> str:
    if readings is None or not iter(readings):
        return str(readings)
    return ", ".join(readings)


def is_valid_kanji_unicode(value: int, /) -> bool:
    return (
        (0x4E00 <= value <= 0x9FFF)  # Common Kanji
        or (0x3400 <= value <= 0x4DBF)  # Extension A
        or (0xF900 <= value <= 0xFAFF)  # Compatibility Kanji
    )


def convert_kanji_to_hex(kanji: str) -> str:
    assert len(kanji) == 1
    kanji_unicode = ord(kanji)
    assert is_valid_kanji_unicode(kanji_unicode)
    return hex(kanji_unicode)


def get_kanji_stroke_order_filepath(kanji: str) -> discord.File:
    root = pathlib.Path(__file__).resolve().parents[2]
    kanji_hex = convert_kanji_to_hex(kanji=kanji).removeprefix("0x")
    filepath = root.joinpath("data", "stroke_orders", f"{kanji_hex}.png")
    return filepath


# Required at the end of all extension modules.
async def setup(bot: commands.Bot, /) -> None:
    await auto_add_cogs(bot)
