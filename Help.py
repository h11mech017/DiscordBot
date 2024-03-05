import discord
from discord import app_commands
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help Cog Ready")
        
    @app_commands.command(name="help", description="顯示所有可用的指令.")
    async def help(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="Help", description="可用指令列表:", color=0x00ff00)
        
            synced_commands = await self.bot.tree.fetch_commands()
            for command in synced_commands:
                embed.add_field(name=f"/{command.name}", value=command.description, inline=False)

            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)

async def setup(bot):
    help_cog = HelpCog(bot)
    await bot.add_cog(help_cog)