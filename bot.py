import asyncio

import discord
from aiologger.loggers.json import JsonLogger
from discord.ext.commands import Bot, MissingRequiredArgument, context

from search import GoogleSearch
from storage import StorageManager

logger = JsonLogger.with_default_handlers(name=__name__)


def initialize_bot(bot: Bot, storage_manager: StorageManager, google_search: GoogleSearch):
    @bot.command()
    async def google(ctx: context.Context, arg):
        '''
        Bot command to let user perform a google search and get top 5 links
        Ex:
        !google node
        !google "game of thrones"
        '''
        # Don't need to wait for the delivery of message hence not using await
        asyncio.create_task(ctx.send(f'Fetching top 5 links for {arg}'))

        # This gives user typing symbol in UI
        with ctx.channel.typing():
            # Google search is not dependent on the storage hence not awaiting it
            asyncio.create_task(storage_manager.save_recent_search(ctx.author.id, arg))

            for link in await google_search.get_top_5_links(arg):
                # The sequence of links matter
                await ctx.send(link)

    @google.error
    async def google_error(ctx, error):
        '''
        Handling google command error
        '''
        logger.warning(f'error on google command {error}')
        if isinstance(error, MissingRequiredArgument):
            await ctx.send('Please give a keyword for google search ....')

    @bot.command()
    async def recent(ctx: context.Context, arg):
        '''
        Bot command to let user find old search keywords partially matching to the current one
        Ex:
        !recent game
        '''
        await ctx.send(f'Similiar keyword searches for "{arg}" are')
        with ctx.channel.typing():
            keywords = await storage_manager.get_recent_searches_for_keyword(ctx.author.id, arg)
            if not keywords:
                await ctx.send(f'No previous search include keyword "{arg}"')
            for keyword in keywords:
                await ctx.send(keyword)

    @recent.error
    async def recent_error(ctx, error):
        '''
        Handling recent command error
        '''
        logger.warning(f'error on recent command {error}')
        if isinstance(error, MissingRequiredArgument):
            await ctx.send('Please give a keyword to match your past searches....')

    @bot.event
    async def on_message(message: discord.Message):
        '''
        Handles the event when someone sends a message
        '''
        # Don't want to process if message is sent by bot itself
        if message.author == bot.user:
            return

        logger.info(f'Got message "{message.content}" from user {message.author}')
        # If message is hi, Hi, HI respond with a hey
        if message.content.lower() == 'hi':
            await message.channel.send('hey')

        # Prcoess the message for a bot command
        await bot.process_commands(message)

    @bot.event
    async def on_guild_join(guild: discord.Guild):
        '''
        Handles the event when bot is added to a guild(server)
        '''
        logger.info(f'bot added in guild {guild.name}')

    @bot.event
    async def on_guild_remove(guild: discord.Guild):
        '''
        Handles the event when bot is removed from a guild(server)
        '''
        logger.info(f'bot removed from guild {guild.name}')

    @bot.event
    async def on_ready():
        '''
        Handles the event when bot is ready to receive further events
        '''
        logger.info(f'{bot.user} has connected to Discord!')
