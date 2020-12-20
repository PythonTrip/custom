import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from .Logger import LogMiddleware

try:
    from .config import *
except Exception as e:
    logging.critical(f"000: {BOT_TOKEN}")



class TelegramBot:
    # def __new__(cls, **kwargs):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(TelegramBot, cls).__new__(cls)
    #     return cls.instance

    def __init__(self, bot_token, admins, storage=MemoryStorage(), parse_mode="HTML"):
        self.bot = Bot(bot_token, parse_mode=parse_mode)
        self.dp = Dispatcher(self.bot, storage=storage, loop=asyncio.get_event_loop())
        self.dp.middleware.setup(LogMiddleware())
        self.settings_tasks = {
            'admins': admins,
            'log': None
        }

    async def shutdown(self):
        await self.dp.storage.close()
        await self.dp.storage.wait_closed()


telegramBot = None
if BOT_TOKEN is None:
    telegramBot = None
else:
    try:
        telegramBot = TelegramBot(BOT_TOKEN, admins)
    except:
        logging.critical(f"001: {BOT_TOKEN}")


# logging.getLogger("matplotlib").setLevel('CRITICAL')
# logging.getLogger("PIL").setLevel('CRITICAL')
# logging.getLogger("concurrent").setLevel('CRITICAL')
# logging.getLogger("aiogram").setLevel('CRITICAL')
# logging.getLogger("asyncio").setLevel('CRITICAL')
# logging.getLogger("aiohttp").setLevel('CRITICAL')
