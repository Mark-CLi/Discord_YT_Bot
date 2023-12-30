import discord
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque

# Declare Intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# Bot command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

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
    'options': '-vn' # Disable video
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

# Queue for songs
song_queue = deque() # Use collections.deque() for thread-safe operations

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
async def from_url(cls, url, *, loop=None, stream=False):
    loop = loop or asyncio.get_event_loop()
    data = None
    try:
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
    except Exception as e:
        print(f"Error occurred while extracting info from url: {e}")
        return None

    if 'entries' in data:
        data = data['entries'][0]

    filename = None
    try:
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        if not filename.endswith('.mp3'):
            filename = f"{filename.rsplit('.', 1)[0]}.mp3"
    except Exception as e:
        print(f"Error occurred while preparing filename: {e}")
        return None

    try:
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    except Exception as e:
        print(f"Error occurred while creating FFmpegPCMAudio: {e}")
        return None

    @classmethod
    async def from_file(cls, file_path):
        return cls(discord.FFmpegPCMAudio(file_path, **ffmpeg_options), title=file_path)

# Ensure these functions are not indented under the class
async def play_next_song(ctx):
    if song_queue:
        next_song = song_queue.popleft()
        await play_song(ctx, next_song)
    else:
        try:
            # Send an embed message indicating the queue is empty and the bot will disconnect in 15 minutes
            embed = discord.Embed(title="Queue Empty", description="The queue is currently empty. Disconnecting in 15 minutes.", color=discord.Color.blue())
            await ctx.send(embed=embed)

            # Wait for 15 minutes
            await asyncio.sleep(15 * 60)  # 15 minutes

            # Disconnect only if the queue is still empty and nothing is playing
            if not song_queue and not ctx.voice_client.is_playing():
                if ctx.voice_client:
                    await ctx.voice_client.disconnect()

        except Exception as e:
            print(f"An error occurred: {e}")

def after_playing(error):
    if not error:
        print("Song finished playing with return code 0. Starting disconnect check.")
        asyncio.run_coroutine_threadsafe(check_queue_and_disconnect(ctx), bot.loop)
    else:
        print(f"Error in playback: {error}")

async def check_queue_and_disconnect(ctx):
    # Wait for 15 minutes, checking the queue state periodically
    for _ in range(15):  # 15 iterations, 1 minute each
        await asyncio.sleep(60)  # Wait 1 minute
        if song_queue or ctx.voice_client.is_playing():
            print("New song added to queue or currently playing. Canceling disconnect.")
            return
    # Disconnect only if the queue is still empty and nothing is playing
    if not song_queue and not ctx.voice_client.is_playing():
        print("Disconnecting after 15 minutes of inactivity.")
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

async def play_song(ctx, song):
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    async with ctx.typing():
        try:
            player = await YTDLSource.from_url(song, loop=bot.loop)
        except Exception as e:
            # If URL is invalid, use ytsearch
            song = f"ytsearch:{song}"
            player = await YTDLSource.from_url(song, loop=bot.loop)

        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx), bot.loop))
        embed = discord.Embed(title="Now Playing", description=player.title, color=discord.Color.blue())
        await ctx.send(embed=embed)

# Make sure the @bot command is aligned with the rest of the commands, not inside any other function
@bot.command(name='play', help='Plays a song from a file or YouTube')
async def play(ctx, *, source):
    song_queue.append(source)
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        await play_song(ctx, song_queue.popleft())
    embed = discord.Embed(title="Added to Queue", description=source, color=discord.Color.green())
    await ctx.send(embed=embed)

@bot.command(name='skip', help='Skips the currently playing song')
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    embed = discord.Embed(title="Song Skipped", description="The current song has been skipped.", color=discord.Color.orange())
    await ctx.send(embed=embed)

@bot.command(name='nuke', help='Clears the entire song queue')
async def nuke(ctx):
    song_queue.clear()
    embed = discord.Embed(title="Queue Nuked", description="The song queue has been cleared.", color=discord.Color.red())
    await ctx.send(embed=embed)

@bot.command(name='queue', help='Shows the current song queue')
async def queue(ctx):
    if song_queue:
        queue_list = '\n'.join(song_queue)
        embed = discord.Embed(title="Current Queue", description=queue_list, color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Queue", description="The queue is currently empty.", color=discord.Color.grey())
        await ctx.send(embed=embed)

@bot.command(name='stop', help='Stops and disconnects the bot from voice')
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    embed = discord.Embed(title="Disconnected", description="The bot has disconnected from the voice channel.", color=discord.Color.dark_red())
    await ctx.send(embed=embed)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('DC BOT TOKEN')
