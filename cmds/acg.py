from discord.ext import commands
from core.classes import Cog_Extension
import function
import random
import cmds.acg_data.data as d
import cmds.acg_data.scraper as scraper
import cmds.acg_data.myself as myself

class ACG(Cog_Extension):
    @commands.group(aliases=['pin'])
    async def pinterest(self, ctx):
        pass

    @pinterest.command()
    async def img(self, ctx):
        url_list = function.open_json('cmds/acg_data/urls.json')['pinterest']
        sent_url = url_list[random.randrange(len(url_list))]
        sent_msg = await ctx.send(sent_url)
        await sent_msg.add_reaction('\u274C')
        function.print_detail(memo='INFO',user=ctx.auther, guild=ctx.guild, channel=ctx.message.channel, obj=f'Send {sent_url}')
        d.url_data(sent_msg, sent_url)
        
    @pinterest.command(aliases=['sp'])
    async def scraper(self, ctx: commands.Context, amount):
        await ctx.send('Start scraping on Pinterest')
        await ctx.send(f'Add {scraper.pinterest(amount=int(amount)).get_pinterest_urls()} pictures')

    @pinterest.command(aliases=['rbm'])
    @commands.is_owner()
    async def resetbm(self, ctx):
        scraper.pinterest.reset_bookmark
        await ctx.send('Reset Pinterest bookmark successfully')
        function.print_detail(memo='INFO',user=ctx.auther, guild=ctx.guild, channel=ctx.message.channel, obj='Reset Pinterest bookmark successfully')

    @commands.group(aliases=['px'])
    async def pixiv(self, ctx):
        pass

    @pixiv.command(aliases=['i', 'pid'])
    async def illust(self, ctx: commands.Context, pid):
        url = scraper.pixiv.get_pixiv_urls_pid(pid)
        for i in range(len(url)):
            await ctx.send(url[i])

    @pixiv.command(aliases=['u', 'uid'])
    async def user(self, ctx: commands.Context, uid):
        r = scraper.pixiv.get_pixiv_urls_uid(uid)
        await ctx.send(f'User name: {r[1]}')
        for key in r[0]:
            url = scraper.pixiv.get_pixiv_urls_pid(key)
            for i in range(len(url)):
                await ctx.send(url[i])
        function.print_detail(memo='INFO',user=ctx.auther, guild=ctx.guild, channel=ctx.message.channel, obj='Scrape complete')

    @commands.group(aliases=['ms'])
    async def myself(self, ctx):
        pass

    @myself.command(aliases=['w'])
    async def week(self, ctx):
        r = myself.Myself.week_animate()
        for day in r:
            text = f'***{day}***\n>>> '
            for anime in r[day]:
                text += f'''{anime['name']} (lastest:{anime['update'][5:-3]})\n<{anime['url']}>\n\n'''
            await ctx.send(text)

    @myself.command(aliases=['a'])
    async def anime(self, ctx: commands.Context, url):
        r = myself.Myself.animate_total_info(url)
        await ctx.send(f'**{r["name"]}：**    *`{r["animate_type"]}`*\n\n`{r["synopsis"]}`\n\n*作者：{r["author"]}*\n*{r["premiere_date"]} 首播*\n*{r["episode"]}*\n\n{r["official_website"]}')
            

async def setup(bot):
    await bot.add_cog(ACG(bot))