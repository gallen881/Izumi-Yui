import asyncio
import discord
from discord.ext import commands
import os
import function

data = function.open_json('data.json')

bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

async def main():

    @bot.event
    async def on_ready():
        function.print_time('Bot is Ready')
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(data['playinggame']))


    @bot.command()
    async def load(ctx, extension):
        await bot.load_extension(f'cmds.{extension}')
        await ctx.send(f'Loaded {extension} successfully')
        function.print_time(f'{extension}.py loaded successfully')

    @bot.command()
    async def unload(ctx, extension):
        await bot.unload_extension(f'cmds.{extension}')
        await ctx.send(f'Unloaded {extension} successfully')
        function.print_time(f'{extension}.py unloaded successfully')

    @bot.command()
    async def reload(ctx, extension):
        await bot.reload_extension(f'cmds.{extension}')
        await ctx.send(f'Reloaded {extension} successfully')
        function.print_time(f'{extension}.py reloaded successfully')

    @bot.command()
    async def version(ctx):
        await ctx.send(f"Version: {data['version']}")

    async with bot:
        for file in os.listdir('./cmds'):
            if file.endswith('.py'):
                await bot.load_extension(f'cmds.{file[:-3]}')
                function.print_time(f'{file} loaded successfully')
        await bot.start(data['token'])

asyncio.run(main())