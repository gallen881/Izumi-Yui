from discord.ext import commands
from core.classes import Cog_Extension
import function
import random
import yaml
import time
import cmds.event_data.form_w as fw
import cmds.acg_data.data as ad
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer



class Events(Cog_Extension):
    langs = ['english', 'chinese', 'japanese', 'self', ]
    chatbot = {}
    for lang in langs:
        chatbot[lang] = ChatBot(lang, database_uri=f'sqlite:///cmds/talk_data/{lang}.database')
        '''ChatterBotCorpusTrainer(chatbot[lang]).train(f'chatterbot.corpus.{lang}')
        function.print_time(f'Training {lang} done')'''

    time_stamp = 0


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.content.startswith('-'):
            return

        data = function.open_json('./cmds/event_data/www.json')
        if message.channel.id not in data['noww_id']:
            if message.content in data["w"] or message.content.endswith('w'):
                rd = random.randrange(10000)
                if rd <= -1:
                    await message.channel.send(fw.form_w('2000'))
                elif rd <= 4130:
                    await message.channel.send(fw.form_w('random'))


        data = function.open_json('./cmds/event_data/synchronous_channel.json')
        if str(message.channel.id) in data.keys():
            for c in data[str(message.channel.id)]:
                ch = self.bot.get_channel(c)
                if message.content != '':
                    await ch.send(f'*{message.author.name}#{message.author.discriminator} sent* **{message.content}** *(from {message.channel})*')

                for attachment in message.attachments:
                    await ch.send(f'*{message.author.name}#{message.author.discriminator} sent (from {message.channel})*')
                    await ch.send(attachment)


        data = function.open_json('./cmds/event_data/listen.json')
        if message.channel.id in data[str(message.guild.id)]:
            path = f'./chatterbot/chatterbot_corpus/data/local/{str(message.channel.id)}.yml'
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    yml = yaml.safe_load(file)
                    file.close()
                existing = True
            except:
                yml = {'categories': [str(message.channel.id)], 'conversations': []}
                existing = False

            now = time.time()
            if now - self.time_stamp > 1800:
                yml['conversations'].append([message.content])
            else:
                try:
                    yml['conversations'][-1].append(message.content)
                except:
                    yml['conversations'].append([message.content])
            self.time_stamp = now
            
            with open(path, 'w', encoding='utf-8') as file:
                yaml.dump(yml, file, allow_unicode=True)
                file.close()

            if existing:
                function.print_time(f'Add {message.content} to an existing conversation')
            else:
                function.print_time(f'Creat a new conversation')


        data = function.open_json('./cmds/talk_data/talk.json')
        if str(message.channel.id) in data.keys():
            async with message.channel.typing():
                responce = self.chatbot[data[str(message.channel.id)]].get_response(message.content)
                await message.channel.send(responce)
            function.print_time(f'{message.author} sent {message.content} bot replied {responce}')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            if payload.emoji.name == '\u274C' and payload.message_id == ad.url_data.msg.id:
                await ad.url_data.msg.delete()
                urls = function.open_json('cmds/acg_data/urls.json')
                urls['pinterest'].remove(ad.url_data.url)
                urls['nopinterest'].append(ad.url_data.url)
                function.write_json('cmds/acg_data/urls.json', urls)

                await self.bot.get_channel(payload.channel_id).send('Deleted picture successfully')

                function.print_time(f'{payload.member} deleted {ad.url_data.url} successfully')
         

async def setup(bot):
    await bot.add_cog(Events(bot))