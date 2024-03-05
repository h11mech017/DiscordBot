from typing import Union
import discord
from discord.ext import commands
from PIL import Image
from emoji import emojify_image
import requests

class Emojify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Emojify Cog Ready")
        
    @commands.command()
    async def emojify(self, ctx, url: Union[discord.Member, str], size: int = 14):
        if not isinstance(url, str):
            url = url.display_avatar.url

        def get_emojified_image():
            r = requests.get(url, stream=True)
            image = Image.open(r.raw).convert("RGB")
            res = emojify_image(image, size)

            if size > 14:
                res = f"```{res}```"
            return res

        result = await self.bot.loop.run_in_executor(None, get_emojified_image)
        await ctx.send(result)

async def setup(bot):
    emojify_cog = Emojify(bot)
    await bot.add_cog(emojify_cog)