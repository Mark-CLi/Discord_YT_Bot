import os
import discord
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque

# Declare Intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

with open('/root/project/production/YTBOT/Discord_Token.txt','r') as file:
    TOKEN = file.read().strip()

# Initialize the bot with application commands
class LurkingintheDark(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        # Register slash commands
        await self.tree.sync()

bot = LurkingintheDark()

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''

# YTDL and FFMPEG options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

# Global Variable
# Queue for songs
song_queue = deque()

# Link Reset
current_song_url = None

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.25):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        if not filename.endswith('.mp3'):
            filename = f"{filename.rsplit('.', 1)[0]}.mp3"

        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

    @classmethod
    async def from_file(cls, file_path):
        return cls(discord.FFmpegPCMAudio(file_path, **ffmpeg_options), title=file_path)

async def play_next_song(interaction):
    if song_queue:
        next_song = song_queue.popleft()
        await play_song(interaction, next_song)
    else:
        try:
            # Send an embed message indicating the queue is empty and the bot will disconnect in 15 minutes
            embed = discord.Embed(title="Queue Empty", description="The queue is empty. Disconnecting in 15 minutes.", color=discord.Color.blue())
            await interaction.followup.send(embed=embed, ephemeral=True)

            # Wait for 15 minutes
            await asyncio.sleep(15 * 60)  # 15 minutes

            # Disconnect only if the queue is still empty and nothing is playing
            if not song_queue and interaction.guild.voice_client and not interaction.guild.voice_client.is_playing():
                await interaction.guild.voice_client.disconnect()

        except Exception as e:
            print(f"An error occurred: {e}")

async def play_song(interaction, song):
    global current_song_url

    if not interaction.guild.voice_client:
        await interaction.user.voice.channel.connect()

    async with interaction.channel.typing():
        try:
            player = await YTDLSource.from_url(song, loop=bot.loop)
        except Exception as e:
            # If URL is invalid, use ytsearch
            song = f"ytsearch:{song}"
            player = await YTDLSource.from_url(song, loop=bot.loop)

        current_song_url = player.url

        interaction.guild.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(interaction), bot.loop))
        embed = discord.Embed(title="Now Playing", description=player.title, color=discord.Color.blue())
        await interaction.followup.send(embed=embed)

# Slash Commands
@bot.tree.command(name='play', description='Plays a song from a file or YouTube')
async def play(interaction: discord.Interaction, source: str):
    await interaction.response.defer()
    song_queue.append(source)
    if not interaction.guild.voice_client or not interaction.guild.voice_client.is_playing():
        await play_song(interaction, song_queue.popleft())
    embed = discord.Embed(title="Added to Queue", description=source, color=discord.Color.green())
    await interaction.followup.send(embed=embed)

@bot.tree.command(name='skip', description='Skips the currently playing song')
async def skip(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.stop()
    embed = discord.Embed(title="Song Skipped", description="The current song has been skipped.", color=discord.Color.orange())
    await interaction.followup.send(embed=embed)

@bot.tree.command(name='nuke', description='Clears the entire song queue')
async def nuke(interaction: discord.Interaction):
    await interaction.response.defer()
    song_queue.clear()
    embed = discord.Embed(title="Queue Nuked", description="The song queue has been cleared.", color=discord.Color.red())
    await interaction.followup.send(embed=embed)

@bot.tree.command(name='queue', description='Shows the current song queue')
async def queue(interaction: discord.Interaction):
    await interaction.response.defer()
    if song_queue:
        queue_list = '\n'.join(song_queue)
        embed = discord.Embed(title="Current Queue", description=queue_list, color=discord.Color.blue())
    else:
        embed = discord.Embed(title="Queue", description="The queue is currently empty.", color=discord.Color.grey())
    await interaction.followup.send(embed=embed)

@bot.tree.command(name='stop', description='Stops and disconnects the bot from voice')
async def stop(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.disconnect()
    embed = discord.Embed(title="Disconnected", description="The bot has disconnected from the voice channel.", color=discord.Color.dark_red())
    await interaction.followup.send(embed=embed)

@bot.tree.command(name='pause', description='Pause the music')
async def pause(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
        interaction.guild.voice_client.pause()
        embed = discord.Embed(title="Paused", description="Song paused", color=discord.Color.orange())
    else:
        embed = discord.Embed(title="Pause Error", description="No song is playing or bot not connected to VC", color=discord.Color.orange())
    await interaction.followup.send(embed=embed)

@bot.tree.command(name='resume', description='Resume the music')
async def resume(interaction: discord.Interaction):
    await interaction.response.defer()
    if interaction.guild.voice_client and interaction.guild.voice_client.is_paused():
        interaction.guild.voice_client.resume()
        embed = discord.Embed(title="Resumed", description="Song Resumed", color=discord.Color.orange())
    else:
        embed = discord.Embed(title="Resume Error", description="No song is playing or bot is not connected to VC", color=discord.Color.orange())
    await interaction.followup.send(embed=embed)

@bot.tree.command(name='link', description='Show the link to the current playing song')
async def link(interaction: discord.Interaction):
    await interaction.response.defer()
    if current_song_url:
        embed = discord.Embed(title="Current Song URL", description=current_song_url, color=discord.Color.blue())
    else:
        embed = discord.Embed(title="No Song is Playing", description="Error, there is no song playing", color=discord.Color.orange())
    await interaction.followup.send(embed=embed)

bot.run(TOKEN)
