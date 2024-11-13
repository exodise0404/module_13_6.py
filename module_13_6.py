from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = InlineKeyboardMarkup()
button = InlineKeyboardMarkup(text = "Рассчитать норму калорий", callback_data = 'calories')
button2 = InlineKeyboardMarkup(text = "Формулы расчёта", callback_data = 'formulas')
kb.add(button, button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)
@dp.callback_query_handler(text = 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    await message.answer(f"Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer(f"Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    Calories = ((10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']))-161)*1.375
    await message.answer(f'Норма калорий: {Calories}')
    await state.finish()

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:')


@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('((10 х вес(кг) + 6.25 х рост(см) - 5 х возраст(лет))-161) х 1.375 (уровень активности)')
    await call.answer()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

