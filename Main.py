import discord
from discord.ext import commands
import yt_dlp
import asyncio

# Declare Intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# Bot command prefix
bot = commands.Bot(command_prefix='!', intents=intents)

# Suppress noise about console usage from errors
yt_dlp.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'extractaudio': True,  # Only keep the audio
    'audioformat': 'mp3',  # Convert to mp3
    'outtmpl': '%(extractor)s-%(title)s.%(ext)s',  # Name the file properly
    'restrictfilenames': True,  # Avoid non-standard characters in file names
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # Take first item from a playlist
            data = data['entries'][0]

        # Ensuring the filename ends with '.mp3'
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        if not filename.endswith('.mp3'):
            filename = f"{filename.rsplit('.', 1)[0]}.mp3"

        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


    @classmethod
    async def from_file(cls, file_path):
        return cls(discord.FFmpegPCMAudio(file_path, **ffmpeg_options), title=file_path)

@bot.command(name='play', help='Plays a song from a file or YouTube')
async def play(ctx, source):
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    async with ctx.typing():
        print(f"Attempting to play from: {source}")  # Log the source path
        if source.startswith("http://") or source.startswith("https://"):
            player = await YTDLSource.from_url(source, loop=bot.loop)
        else:
            player = await YTDLSource.from_file(source)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

    await ctx.send(f'Now playing: {player.title}')


@bot.command(name='stop', help='Stops and disconnects the bot from voice')
async def stop(ctx):
    await ctx.voice_client.disconnect()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token

bot.run('Token')
