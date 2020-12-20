import sys
from misc import telegramBot
from aiogram import executor
import handlers


async def send_to_admin(*args):
    [await telegramBot.bot.send_message(chat_id=admin_id, text="Бот запущен") for admin_id in
     telegramBot.settings_tasks['admins']]


if __name__ == '__main__':
    executor.start_polling(telegramBot.dp, skip_updates=True, on_startup=send_to_admin)
