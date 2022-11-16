from discord.ext import commands
from core.classes import Cog_Extension
import function

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class Talk(Cog_Extension):


    chatbot = {}


    @commands.command()
    @commands.is_owner()
    async def listen(self, ctx: commands.Context):
        data = function.open_json('./cmds/events_data/listen.json')
        if str(ctx.guild.id) in data.keys():
            if ctx.channel.id not in data[str(ctx.guild.id)]:
                data[str(ctx.guild.id)].append(ctx.channel.id)
                write = True
            else:
                write = False
        else:
            data[str(ctx.guild.id)] = [ctx.channel.id]
            write = True
        
        if write:
            function.write_json('./cmds/events_data/listen.json', data)
            function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj='Start to listen on')


    @commands.command()
    @commands.is_owner()
    async def nolisten(self, ctx: commands.Context):
        data = function.open_json('./cmds/events_data/listen.json')
        try:
            data[str(ctx.guild.id)].remove(ctx.channel.id)
        except:
            pass

        function.write_json('./cmds/events_data/listen.json', data)
        function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj='Stop listening')


        
    @commands.command()
    async def chat(self, ctx: commands.Context, lang=''):
        talk = function.open_json('./cmds/talk_data/talk.json')
        if lang == '':
            talk[str(ctx.channel.id)] = f'local.{ctx.channel.id}'
            lang = f'local.{ctx.channel.id}'
        else:
            talk[str(ctx.channel.id)] = lang
        function.write_json('./cmds/talk_data/talk.json', talk)
        self.chatbot[lang] = ChatBot(lang, database_uri=f'sqlite:///cmds/talk_data/{lang}.database')
        function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj='Chat on')

    
    @commands.command()
    async def nochat(self, ctx: commands.Context):
        talk = function.open_json('./cmds/talk_data/talk.json')
        del talk[str(ctx.message.channel.id)]
        function.write_json('./cmds/talk_data/talk.json', talk)
        function.print_detail(memo='INFO',user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj='Chat off')


    @commands.command()
    @commands.is_owner()
    async def train(self, ctx: commands.Context, lang=''):
        if lang == '':
            lang = f'local.{ctx.channel.id}'
        ChatterBotCorpusTrainer(self.chatbot[lang]).train(f'chatterbot.corpus.{lang}')


    

async def setup(bot):
    await bot.add_cog(Talk(bot))