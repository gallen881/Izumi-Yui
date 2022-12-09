from discord.ext import commands
import youtube_dl
import asyncio
import discord
import nacl

from core.classes import Cog_Extension
import core.function as function

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
    async def from_url(self, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


class Music(Cog_Extension):
    PlayList = {}
    @commands.command()
    async def join(self, ctx: commands.Context):
        if not ctx.message.author.voice:
            await ctx.send('You is not connected to a voice channel')
        else:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'Join successfully')


    @commands.command(aliases=['p'])
    async def play(self, ctx: commands.Context, url):
        voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client == None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'Join successfully')
            voice_client: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        print(1, voice_client)

        c_id = str(ctx.channel.id)
        if c_id not in self.PlayList.keys():
            self.PlayList[c_id] = []
        print(2, c_id,self.PlayList, self.PlayList[c_id])

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=self.bot.loop)
        print(3, filename)

        if self.PlayList[c_id] == []:
            print(4)
            self.PlayList[c_id] = [filename]
            print(41)
            await self.playing(voice_client, c_id)


        else:
            print(55)
            try:
                self.PlayList[c_id][len(self.PlayList)] = filename
                print('tr')
            except:
                self.PlayList[c_id].append(filename)
                print('ex')
            print(5)

    async def playing(self, voice_client, c_id):
        voice_client.play(discord.FFmpegPCMAudio(source=self.PlayList[c_id][0]))
        print('d')
        del self.PlayList[c_id][0]
        print('do')
        
        self.playing(self, voice_client, c_id)


    @commands.command(aliases=['q'])
    @commands.is_owner()
    async def queue(self, ctx):
        await ctx.send(self.PlayList[str(ctx.channel.id)])
async def setup(bot):
    await bot.add_cog(Music(bot))