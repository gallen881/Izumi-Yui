from discord.ext import commands
import random

from core.classes import Cog_Extension
import core.function as function
import func.temp as d
import func.scraper as scraper


class ACG(Cog_Extension):
    @commands.group(aliases=['pin'])
    async def pinterest(self, ctx):
        pass

    @pinterest.command()
    async def img(self, ctx: commands.Context):
        url_list = function.open_json('./data/urls.json')['pinterest']
        sent_url = url_list[random.randrange(len(url_list))]
        sent_msg = await ctx.send(sent_url)
        await sent_msg.add_reaction('\u274C')
        function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'Send {sent_url}')
        d.url_data(sent_msg, sent_url)
        
    @pinterest.command(aliases=['sp'])
    async def scraper(self, ctx: commands.Context, amount: int):
        await ctx.send('Start scraping on Pinterest')
        await ctx.send(f'Add {scraper.Pinterest(amount=amount).get_pinterest_urls()} pictures')

    @pinterest.command(aliases=['rbm'])
    @commands.is_owner()
    async def resetbm(self, ctx: commands.Context):
        scraper.Pinterest.reset_bookmark
        await ctx.send('Reset Pinterest bookmark successfully')
        function.print_detail(memo='INFO', user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj='Reset Pinterest bookmark successfully')

    @commands.group(aliases=['px'])
    async def pixiv(self, ctx):
        pass

    @pixiv.command(aliases=['i', 'pid'])
    async def illust(self, ctx: commands.Context, pid):
        url = scraper.Pixiv.get_pixiv_urls_pid(pid)
        for i in range(len(url)):
            await ctx.send(url[i])

    @pixiv.command(aliases=['u', 'uid'])
    async def user(self, ctx: commands.Context, uid):
        r = scraper.Pixiv.get_pixiv_urls_uid(uid)
        await ctx.send(f'User name: {r[1]}')
        for key in r[0]:
            url = scraper.Pixiv.get_pixiv_urls_pid(key)
            for i in range(len(url)):
                await ctx.send(url[i])
        function.print_detail(memo='INFO', user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj='Scrape complete')

            

async def setup(bot):
    await bot.add_cog(ACG(bot))