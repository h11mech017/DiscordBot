import discord

intents = discord.Intents.default()
intents.typing = True
intents.presences = False
intents.message_content = True