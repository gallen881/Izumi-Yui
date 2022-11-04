from discord.ext import commands
from core.classes import Cog_Extension
import function
import youtube_dl
import asyncio
import discord
import nacl

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

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
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


class Music(Cog_Extension):
    def __call__(self, vc):
        self.vc = vc
    @commands.command()
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send('You is not connected to a voice channel')
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()


    @commands.command()
    async def play(self, ctx, url):
        try :
            voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            print(voice_client)
            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=self.bot.loop)
                print(1)
                voice_client.play(discord.FFmpegPCMAudio(source=filename))
            await ctx.send(f'**Now playing: ** `{filename}`')
        except:
            pass


async def setup(bot):
    await bot.add_cog(Music(bot))