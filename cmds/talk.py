from discord.ext import commands
from core.classes import Cog_Extension
import function

class Talk(Cog_Extension):


    @commands.command()
    @commands.is_owner()
    async def listen(self, ctx):
        data = function.open_json('./cmds/event_data/listen.json')
        if str(ctx.guild.id) in data.keys():
            data[str(ctx.guild.id)].append(ctx.channel.id)
        else:
            data[str(ctx.guild.id)] = [ctx.channel.id]
        function.write_json('./cmds/event_data/listen.json', data)

        function.print_time(f'Start to listen on {ctx.channel}({ctx.guild})')

        
    @commands.command()
    async def chat(self, ctx, lang=True):
        talk = function.open_json('./cmds/talk_data/talk.json')
        if lang:
            talk[str(ctx.message.channel.id)] = f'local.{str(ctx.channel.id)}'
        else:
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