import discord
from discord.ext import commands
from core.classes import Cog_Extension
import function
import cmds.tools_data.bullshit.bullshit as bt
import cmds.tools_data.scraper as scraper
import cmds.tools_data.img.img as img

class Tools(Cog_Extension):
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'ping: {self.bot.latency * 1000} (ms)')


    @commands.command()
    async def getchannelid(self, ctx: commands.Context):
        await ctx.send(f'This channel id is {ctx.channel.id}')

    
    @commands.command()
    async def say(self, ctx: commands.Context, *messages):
        texts = ''
        for message in messages:
            texts += message + ' '
        for text in function.split_str_to_list(texts, 2000):
            await ctx.send(text)
            function.print_detail(memo='INFO', user=ctx.author, guild=ctx.guild, channel=ctx.channel, obj=f'Send "{text}"')


    @commands.command()
    async def bullshit(self, ctx: commands.Context, title: str, length: int):
        bullshits = bt.generate(title, length)
        bl = function.split_str_to_list(bullshits, 1994)
        for bullshit in bl:
            await ctx.send(f'```{bullshit}```')
        function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'Send "{bullshits}"')

    @commands.command()
    async def eqinfo(self, ctx: commands.Context, eq: int):
        data = scraper.scrap_eq(eq)
        combination = f'{data[0]}，芮氏規模 {data[1]} 級，深度 {data[2]} 公里，發生時間 {data[3]}'
        await ctx.send(combination)
        await ctx.send(data[4])

        function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'Send {combination}')
        function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'Send {data[4]}')

    @commands.command()
    async def eqgif(self, ctx):
        await ctx.send('https://tenor.com/view/jumprooe-earthquake-gif-15657117')
        function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj='Send https://tenor.com/view/jumprooe-earthquake-gif-15657117')

    @commands.command()
    async def synce(self, ctx: commands.Context, *ch_ids):
        data = function.open_json('./cmds/events_data/synchronous_channel.json')
        if str(ctx.channel.id) in data.keys():
            for ch_id in ch_ids:
                if ch_id not in str(data[str(ctx.channel.id)]):
                    data[str(ctx.channel.id)].append(int(ch_id))
                    await ctx.send(f'Synce {ch_id} successfully')
        else:
            data[str(ctx.channel.id)] = []
            for ch_id in ch_ids:
                data[str(ctx.channel.id)].append(int(ch_id))
                await ctx.send(f'Synce {ch_id} successfully')

        function.write_json('./cmds/events_data/synchronous_channel.json', data)


    @commands.command()
    async def nosynce(self, ctx: commands.Context, *ch_ids):
        data = function.open_json('./cmds/events_data/synchronous_channel.json')

        if str(ctx.channel.id) in data.keys():
            for ch_id in ch_ids:
                if int(ch_id) in data[str(ctx.channel.id)]:
                    data[str(ctx.channel.id)].remove(int(ch_id))
                    await ctx.send(f'Disable synce to {ch_id} successfully')

        function.write_json('./cmds/events_data/synchronous_channel.json', data)

    @commands.group()
    async def img(self, ctx):
        pass

    @img.command()
    async def ocr(self, ctx: commands.Context, lang: str, *urls):
        for attachment in ctx.message.attachments:
            for text in img.ocr(attachment, lang):
                await ctx.reply(text)
                function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'Send {text}')

        if urls != []:
            for url in urls:
                for text in img.ocr(url, lang):
                    await ctx.reply(text)
                    function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'Send {text}')
    @img.command(aliases=['r'])
    async def rotate(self, ctx: commands.Context, angle: float, url=None):
        for attachment in ctx.message.attachments:
            img.rotate(attachment, float(angle))
            await ctx.reply(file=discord.File('./cmds/tools_data/img/temp.png'))

        if url != None:
            img.rotate(url, float(angle))
            await ctx.reply(file=discord.File('./cmds/tools_data/img/temp.png'))
            function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj='Send temp.png')


    @img.command(aliases=['g'])
    async def generate(self, ctx: commands.Context, *prompt):
        texts = ''
        for message in prompt:
            texts += message + ' '
        await ctx.send(img.generate(texts))


async def setup(bot):
    await bot.add_cog(Tools(bot))
