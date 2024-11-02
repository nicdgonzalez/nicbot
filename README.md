# NicBot

A personal, general-purpose bot that runs on Discord.

## Getting Started

**Python 3.12 or higher is required.**

First, clone the project onto your machine:

```bash
git clone https://github.com/nicdgonzalez/nicbot && cd nicbot
```

Then, install dependencies. (I use [uv] to manage my Python projects.)

```bash
# with uv
uv venv && source .venv/bin/activate
uv sync

# with python
python -m venv .venv && source .venv/bin/activate
# pip will install the project as a package along with all of its dependencies.
# Since we just want the dependencies, we uninstall immediately afterwards.
python -m pip install . && python -m pip uninstall .
```

Get a Discord API key from the [Discord Developer Portal], then paste it into
the `.env` file:

> [!TIP]
> Need help creating the bot up and getting your bot token? Try the
> ["Getting started" section of the discord.py documentation].

```bash
echo "DISCORD_TOKEN=<your.bot.token>" >> .env
```

Log messages will be sent to the `logs` directory in the root of the project
(i.e., the same level as the `nicbot` directory and this README). By default,
it only writes warnings and errors, but you can use the `--verbose` or `-v`
flag to write "info" level logs as well. This flag stacks, so use it twice to
also print "debug" level logs.

```bash
# to write INFO level log messages:
python -m nicbot --verbose

# to write DEBUG level log messages:
python -m nicbot --verbose --verbose

# or,
python -m nicbot -vv
```

<!-- TODO: Use pydoc or sphinx to generate proper documentation -->
For additional documentation, check the source code.

<!-- IGNORE -->

[uv]: https://github.com/astral-sh/uv
["Getting started" section of the discord.py documentation]: https://discordpy.readthedocs.io/en/latest/index.html#getting-started
