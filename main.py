import settings
import os
from dotenv import load_dotenv
import subprocess
from discord.ext import commands
import asyncio

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=settings.intents, help_command=None)


@bot.event
async def on_ready():
    print("Bot Ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)

async def main():
    async with bot:
        # subprocess.run(os.getenv('COMMAND'), shell=True, check=True)
        await bot.load_extension("MusicPlayer")
        await bot.load_extension("Emojify")
        await bot.load_extension("Help")
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())