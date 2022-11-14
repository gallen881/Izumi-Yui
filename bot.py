import keep_alive

VERSION = '6.4.0'

import asyncio
import discord
from discord.ext import commands
import os
import function

bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

async def main():


    @bot.event
    async def on_ready():
        function.print_detail(memo='INFO', obj='Bot is Ready')
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(function.open_json('data.json')['playinggame']))


    @bot.command()
    @commands.is_owner()
    async def load(ctx, extension):
        await bot.load_extension(f'cmds.{extension}')
        await ctx.send(f'Loaded {extension} successfully')
        function.print_detail(memo='INFO',user=ctx.user, guild=ctx.guild, channel=ctx.message.channel, obj=f'{extension}.py loaded successfully')

    @bot.command(aliases=['ul'])
    @commands.is_owner()
    async def unload(ctx, extension):
        await bot.unload_extension(f'cmds.{extension}')
        await ctx.send(f'Unloaded {extension} successfully')
        function.print_detail(memo='INFO',user=ctx.user, guild=ctx.guild, channel=ctx.message.channel, obj=f'{extension}.py unloaded successfully')

    @bot.command(aliases=['rl'])
    @commands.is_owner()
    async def reload(ctx, extension):
        await bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f'Reloaded {extension} successfully')
        function.print_detail(memo='INFO', user=ctx.author, guild=ctx.guild, channel=ctx.message.channel, obj=f'{extension}.py reloaded successfully')

    @bot.command(aliases=['info'])
    async def infomations(ctx):
        data = function.open_json("data.json")
        text =''
        for i, features in enumerate(data['new_features']):
            text += f'    *{i + 1}. {features}*\n'
        await ctx.send(f'**Version:** *{VERSION}*\n**New features:** \n{text}**GitHub:** *{data["github"]}*')

    async with bot:
        for file in os.listdir('./cmds'):
            if file.endswith('.py') and file != 'data.py':
                await bot.load_extension(f'cmds.{file[:-3]}')
                function.print_detail(memo='INFO', obj=f'{file} loaded successfully')
        keep_alive.keep_alive()
        await bot.start(function.open_json('data.json')['token'])

asyncio.run(main())