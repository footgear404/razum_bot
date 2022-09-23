import logging
from aiogram import Bot, types
from aiogram.types import InputMediaPhoto
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import TOKEN
from states.ClientRateState import GetFeedBack
from messages import MESSAGES

# logging here
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())

users = [341031421]


# commands here
@dp.message_handler(commands=['start'])
async def usrReg(message: types.Message, state: FSMContext):
    await message.answer(MESSAGES['start'])


@dp.message_handler(commands=['help'])
async def usrReg(message: types.Message, state: FSMContext):
    await message.answer(MESSAGES['help'])


@dp.message_handler(commands=['reg'])
async def usrReg(message: types.Message, state: FSMContext):
    # message.get_args() - get args of commands
    await message.answer("Введите своё имя")
    await GetFeedBack.NAME.set()


@dp.message_handler(state=GetFeedBack.NAME)
async def getUsrName(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отлично! Теперь введите ваш номер телефона.")
    await GetFeedBack.next()


@dp.message_handler(state=GetFeedBack.PHONE)
async def second_test_state_case_met(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Отлично! Дайте нам оценку от 1 до 10 (1- плохо, 10- отлично).")
    await GetFeedBack.next()


@dp.message_handler(state=GetFeedBack.RATE)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(rate=message.text)
    data = await state.get_data()
    await message.answer(f"Имя: {data['name']}\n"
                         f"Тел: {data['phone']}\n"
                         f"Оценка: {data['rate']}")
    await state.finish()


@dp.message_handler()
@dp.edited_message_handler(content_types=['text'])
async def echo_message(message: types.Message):
    # await bot.send_message('341031421', "message here")
    # media = ''
    # try:
    #     media = [InputMediaPhoto(message.photo[-1], message.text)]
    # except Exception as e:
    #     print(e)
    if message.from_user.id == 341031421:
        for user in users:
            print(user)
            await bot.send_message(user, message.text)
    else:
        print(str(message.from_user.id) + 'Else')


# @dp.message_handler()
# @dp.edited_message_handler(content_types=['text'])
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
