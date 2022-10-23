from discord.ext import commands
from core.classes import Cog_Extension
import random
import function
import cmds.event_data.form_w as fw
import cmds.acg_data.data as d


class Events(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self, message):
        function.print_time(f'{message.author} sent {message.content}')
        if message.author == self.bot.user:
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

                

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            if payload.emoji.name == '\u274C' and payload.message_id == d.msg.id:
                await d.msg.delete()
                urls = function.open_json('cmds/acg_data/urls.json')
                urls['pinterest'].remove(d.url)
                urls['nopinterest'].append(d.url)
                function.write_json('cmds/acg_data/urls.json', urls)

                await self.bot.get_channel(payload.channel_id).send('Deleted picture successfully')

                function.print_time(f'{payload.member} deleted {d.url} successfully')

            
            # 

            d = function.open_json('./cmds/event_data/emoji_role.json')
            print(1)
            if payload.message_id in d['message_id']:
                print(2)
                if payload.emoji.name in d['emoji_role'].keys():
                    print(3)
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(d['emoji_role'][payload.emoji.name])
                    role2 = guild.get_role(d['emoji_role']['all'])
                    user = payload.member
                    print(4)
                    await user.add_roles(role, role2)
                    print(5)
                    function.print_time(f'Add {role} which is in {guild} to {user}')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
            d = function.open_json('./cmds/event_data/emoji_role.json')
            print(1)
            if payload.message_id in d['message_id']:
                print(2)
                if payload.emoji.name in d['emoji_role'].keys():
                    print(3)
                    guild = self.bot.get_guild(payload.guild_id)
                    role = guild.get_role(d['emoji_role'][payload.emoji.name])
                    role2 = guild.get_role(d['emoji_role']['all'])
                    user = self.bot.get_user(payload.user_id)
                    print(4)
                    print(guild, role, role2, user)
                    await user.remove_roles(role, role2)
                    print(5)
                    function.print_time(f'Remove {role} which is in {guild} to {user}')

            

async def setup(bot):
    await bot.add_cog(Events(bot))