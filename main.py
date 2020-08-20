import asyncio
import signal

from aiologger.loggers.json import JsonLogger
from discord.ext.commands import Bot

from bot import initialize_bot, logger
from search import GoogleSearch
from settings import settings
from storage import get_storage_manager

logger = JsonLogger.with_default_handlers(name=__name__)


async def main():
    storage_manager = get_storage_manager('redis')
    async with GoogleSearch() as google_search:
        bot = Bot(command_prefix='!')
        initialize_bot(bot, storage_manager, google_search)
        try:
            await bot.start(settings.TOKEN)
        finally:
            await bot.close()


if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    def stop_loop_on_completion(f):
        loop.stop()

    # Various handling to gracefully stop the event loop
    try:
        loop.add_signal_handler(signal.SIGINT, lambda: loop.stop())
        loop.add_signal_handler(signal.SIGTERM, lambda: loop.stop())
    except NotImplementedError:
        pass

    future = asyncio.ensure_future(main(), loop=loop)
    future.add_done_callback(stop_loop_on_completion)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Received signal to terminate bot and event loop.')
    finally:
        future.remove_done_callback(stop_loop_on_completion)
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
