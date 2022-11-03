from core.classes import Cog_Extension
from discord.ext import commands
import discord
import function

class Test(Cog_Extension):
    @commands.command()
    async def test(self, ctx):
        list = ['🔘', '🔴', '🟠', '🟡', '🟢', '🔵', '🟣', '🟤', '⚫', '⚪', '🟥', '🟧', '🟨', '🟩', '🟦', '🟪', '🟫', '⬛', '⬜', '🔶', '🔷', '🔲', '🔳', '▪️']
        list2 = ['附中', '政大附中', '大安', '景美', '松山', '中山', '復興', '木柵', '中正', '建中', '基隆高中', '南湖', '三民', '北一', '成功', '松山工農', '內湖', '新店', '成淵', '大同', '海山', '西松', '弘文', '巨人']
        l = []
        print('ok')
        for i in range(25):
            send = await ctx.send(f'這裡是**{list2[i]}**：{list[i]}')
            await send.add_reaction(list[i])
            print(send.id)
            l.append(send.id)
            print(l)
            dict = function.open_json('./cmds/event_data/emoji_role.json')
            dict['message_id'] = l
            function.write_json('./cmds/event_data/emoji_role.json', dict)

    @commands.command()
    async def tell(self, ctx):
        await ctx.send('革命性的時代已經到來，放下包袱，踏上旅程吧')
        await ctx.remove
            

async def setup(bot):
    await bot.add_cog(Test(bot))