from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from misc import telegramBot

available_food_names = ["суши", "спагетти", "хачапури"]
available_food_sizes = ["маленькую", "среднюю", "большую"]


class OrderFood(StatesGroup):
    waiting_for_food_name = State()
    waiting_for_food_size = State()


@telegramBot.dp.message_handler(commands=["food", "еда"], state="*")
async def food_step_1(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in available_food_names:
        keyboard.add(name)
    await message.answer("Выберите блюдо:", reply_markup=keyboard)
    await OrderFood.waiting_for_food_name.set()


@telegramBot.dp.message_handler(state=OrderFood.waiting_for_food_name, content_types=types.ContentTypes.TEXT)
async def food_step_2(message: types.Message, state: FSMContext):  # обратите внимание, есть второй аргумент
    if message.text.lower() not in available_food_names:
        await message.reply("Пожалуйста, выберите блюдо, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_food=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for size in available_food_sizes:
        keyboard.add(size)
    await OrderFood.next()  # для простых шагов можно не указывать название состояния, обходясь next()
    await message.answer("Теперь выберите размер порции:", reply_markup=keyboard)


@telegramBot.dp.message_handler(state=OrderFood.waiting_for_food_size, content_types=types.ContentTypes.TEXT)
async def food_step_3(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_food_sizes:
        await message.reply("Пожалуйста, выберите размер порции, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    await message.answer(f"Вы заказали {message.text.lower()} порцию {user_data['chosen_food']}.\n"
                         f"Попробуйте теперь заказать напитки: /drinks", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
