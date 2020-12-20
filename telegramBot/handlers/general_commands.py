from aiogram.types import Message, BotCommand, ParseMode
from misc import telegramBot
from Models import FunctionsHandle, NLP
from numpy import *
from aiogram.utils.markdown import text, bold, italic, code, pre

fh = FunctionsHandle()


def admin_control(func):
    async def wrapper(message: Message):
        if message['from']["id"] in telegramBot.settings_tasks['admins']:
            return await func(message)
        return False

    return wrapper


@telegramBot.dp.message_handler(commands=["start", "help"])
async def h_start(message: Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    msg = text(bold('Я могу ответить на следующие команды:'),
               '/math sqrt(25) -> 5', '/pfunc function,x0,x1,epsilon -> png', '/q text', '/a text', sep='\n')
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN)
    # await message.reply(
    #     "TEST BOT\n\n"
    #     "Math functions: /math sqrt(25) -> 5\n"
    #     "Create plot of function: /pfunc function,x0,x1,epsilon -> png\n"
    #     "Add question: /q text\n"
    #     "Add answer: /a text\n"
    # )


async def set_command(message: Message, new_commands):
    commands = [command.split(',') for command in new_commands.split(';')]
    if len(commands[::-1][0]) == 1: commands = commands[::-1][1:]
    await telegramBot.bot.set_my_commands(
        [BotCommand(command=command[0], description=command[1]) for command in commands])
    await message.answer("Команды настроены.")


setting_commands = {
    "set_command": set_command
}


@telegramBot.dp.message_handler(commands=["settings"])
@admin_control
async def h_settings(message: Message):
    task = message.text.replace("/settings", "").split(":")
    task = [t.strip() for t in task]
    await setting_commands[f"{task[0]}"](message, task[1])
    print("Hello admin")


@telegramBot.dp.message_handler(commands=["math"])
async def h_math(message: Message):
    task = message.text.replace("/math", "").lower()
    await message.reply(eval(f"{task}"))


@telegramBot.dp.message_handler(commands=["q"])
async def h_question(message: Message):
    NLP.set_question(message.text.replace("/q", "").lower(), message.chat.id)
    await message.answer("Question has added")


@telegramBot.dp.message_handler(commands=["a"])
async def h_answer(message: Message):
    if NLP.set_answer(message.text.replace("/a", "").lower(), message.chat.id):
        await message.answer("Answer has added")
    else:
        await message.answer("Not question")


@telegramBot.dp.message_handler(commands=["pfunc2d"])
async def h_pfunc2d(message: Message):
    task = message.text.replace("/pfunc2d", "").split(',')
    print(message)
    print(task)
    fh.create_func(task[0], task[1], task[2], epsilon=0.1 if len(task) < 4 else float(task[3]))
    if fh.create_plot():
        await message.answer_photo(photo=open('pic.png', 'rb'))
    else:
        await message.reply(f"Create function")
