import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import wavelink

load_dotenv()

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    channel_id: int 

    @commands.Cog.listener()
    async def on_ready(self):
        nodes = [wavelink.Node(uri=os.getenv('HOST'), password=os.getenv('PW'))]
        await wavelink.Pool.connect(nodes=nodes, client=self.bot, cache_capacity=100)
        wavelink.AutoPlayMode.enabled
        print("Music Cog Ready")

    @commands.Cog.listener()
    async def on_connect(self):
        if self.bot.voice_client:
            self.channel_id = self.bot.voice_client.channel.id


    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
        try:
            channel = payload.player.guild.get_channel(self.channel_id)
            if channel:
                await channel.send(f"現正播放: {payload.player.current}", delete_after=200)
            else:
                print(f"Channel with ID: {self.channel_id} not found.")
        except Exception as e:
            print(e)
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEndEventPayload):
        if not payload.player.queue:
            channel = payload.player.guild.get_channel(self.channel_id)
            await channel.send("已播放所有歌曲: 我嘅任務已經完成了", delete_after=40)
            await payload.player.disconnect()
        else:
            await payload.player.play(payload.player.queue.get())

    @app_commands.command(name="join", description="加入用戶所在頻道.")
    async def join(self, interaction: discord.Interaction):
        await interaction.user.voice.channel.connect()
        await interaction.response.send_message("我要進來嘍𓁹‿𓁹")

    @app_commands.command(name="disconnect", description="離開用戶所在頻道.")
    async def disconnect(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        await vc.disconnect()
        await interaction.response.send_message("已離開頻道.")

    @app_commands.command(name="play", description="播放歌曲, 用法: '/play 關鍵字' 或 '/play 連結'.")
    async def play(self, interaction: discord.Interaction, search: str):
        try:
            destination = interaction.user.voice.channel
            tracks: wavelink.Search = await wavelink.Playable.search(search, source="ytsearch")

            if not interaction.guild.voice_client:
                vc = await destination.connect(cls=wavelink.Player)
            else:
                vc = interaction.guild.voice_client

            if isinstance(tracks, wavelink.Playlist):
                added: int = await vc.queue.put_wait(tracks)
                await interaction.response.send_message(f"己新增{added}首歌到隊列 ({tracks.name}).")
            else:
                track: wavelink.Playable = tracks[0]
                await vc.queue.put_wait(track)
                await interaction.response.send_message(f"{track} 已加入隊列.", delete_after=40)
                
            if not vc.playing:
                self.channel_id = interaction.channel_id
                await vc.play(vc.queue.get())

        except Exception as e:
            print(e)
            await interaction.response.send_message("播放時出現錯誤.")

    @app_commands.command(name="stop", description="停止播放所有歌曲.")
    async def stop(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        await vc.skip()
        await vc.disconnect()
        await interaction.response.send_message("已停止播放.")

    @app_commands.command(name="pause", description="暫停目前歌曲.")
    async def pause(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        await vc.pause(True)
        await interaction.response.send_message("歌曲已暫停.")

    @app_commands.command(name="resume", description="繼續播放目前歌曲.")
    async def resume(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc.paused:
            await vc.pause(False)
            await interaction.response.send_message("歌曲繼續播放.")
        else:
            await interaction.response.send_message("歌曲已經在播放中.")

    @app_commands.command(name="skip", description="跳過目前歌曲.")
    async def skip(self, interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        await vc.skip()
        await interaction.response.send_message("已跳過目前歌曲.")

    @app_commands.command(name="queue", description="顯示所有在隊列中的歌曲.")
    async def queue(self, interaction: discord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        channel = vc.guild.get_channel(self.channel_id)
        if not vc.queue.is_empty:
            queue_counter = 1
            queue = []
            await interaction.response.send_message(f"目前隊列中的歌有{vc.queue.count}首: \n")
            for item in vc.queue:
                queue.append(f"{queue_counter}. {item}")
                queue_counter += 1
            queue_list = "\n".join(queue)
            await channel.send(queue_list)
        else:
            await interaction.response.send_message("目前沒有歌曲在隊列中.")


async def setup(bot):
    music_cog = MusicCog(bot)
    await bot.add_cog(music_cog)
