from discord.ext import commands
from core.classes import Cog_Extension
import function

class Talk(Cog_Extension):

    @commands.command()
    async def chat(self, ctx, lang):
        talk = function.open_json('./cmds/talk_data/talk.json')
        talk[str(ctx.message.channel.id)] = lang
        function.write_json('./cmds/talk_data/talk.json', talk)
        function.print_time(f'{ctx.channel}({ctx.channel.id}) chat on')

    
    @commands.command()
    async def nochat(self, ctx):
        talk = function.open_json('./cmds/talk_data/talk.json')
        del talk[str(ctx.message.channel.id)]
        function.write_json('./cmds/talk_data/talk.json', talk)
        function.print_time(f'{ctx.channel}({ctx.channel.id}) chat off')

    

async def setup(bot):
    await bot.add_cog(Talk(bot))