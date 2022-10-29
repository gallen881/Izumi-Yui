from discord.ext import commands
from core.classes import Cog_Extension
import function

class Talk(Cog_Extension):

    @commands.command()
    async def talk(self, ctx, lang):
        talk = function.open_json('./cmds/talk_data/talk.json')
        talk[str(ctx.message.channel.id)] = lang
        function.write_json('./cmds/talk_data/talk.json', talk)
        function.print_time(f'{ctx.channel}({ctx.channel.id}) chat on')

async def setup(bot):
    await bot.add_cog(Talk(bot))