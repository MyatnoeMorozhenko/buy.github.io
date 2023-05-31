#BOT Name = Korean grandma
#https://t.me/koreangrandma_bot

import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from client_keyb import keyb_client
from client_keyb import keyb_client2
from client_keyb import keyb_client3
from client_keyb import keyb_client_set
from client_keyb import keyb_client_menu
from client_keyb import keyb_client_level1
from client_keyb import keyb_client_level1_back
import json
from parser.parser import check_news_updates
from dotenv import load_dotenv
from db import database as db
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import ReplyKeyboardMarkup


load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)


f = open('enterylevel/Урок1.txt', encoding='utf-8')
u1 = f.read()
f.close()

fi = open('Инструкция', encoding='utf-8')
instruction = fi.read()
fi.close()

f2 = open('enterylevel/Урок2', encoding='utf-8')
u2 = f2.read()
f2.close()

f3 = open('enterylevel/Урок3', encoding='utf-8')
u3 = f3.read()
f3.close()

f4 = open('enterylevel/Урок4', encoding='utf-8')
u4 = f4.read()
f4.close()

f5 = open('enterylevel/Урок5', encoding='utf-8')
u5 = f5.read()
f5.close()

#Дата база

async def on_startup(_):
    await db.db_start()
    print('База создана!')

@dp.message_handler(commands=['start'])
async def command_start(msg: types.Message):
    await db.cmd_start_db(msg.from_user.id)
    """await db.cmd_start_db_name(msg.from_user.username)"""
    await bot.send_message(msg.from_user.id,
                           f'Привет,{msg.from_user.full_name}! Это бот для изучения корейского языка. Для перехода к обучению нажми "Меню уроков".',
                           reply_markup=keyb_client)


@dp.message_handler(commands=['menu'])
async def command_start(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Вы вернулись в главное меню.', reply_markup=keyb_client)


#Домашние задания
photo = open('/Users/alenaagafonova/PycharmProjects/?Korean/db/sejong1.png', 'rb')


@dp.callback_query_handler(lambda call: call.data == 'button6')
async def command_start(call):
    await bot.send_photo(call.from_user.id,
                         caption='<b>Задание 1</b>\nЗаполните все поля в соответсвии с примером. Можете написать в тетради или же попрактиковаться в сочетании клавиш на клавиатуре.',
                         parse_mode='HTML', photo=photo)


@dp.callback_query_handler(lambda c: True)
async def settings(callback_query: types.CallbackQuery):
    # await bot.edit_message_text(callback_query.chat.id, message.id = callback_query.msg.id, text = 'ghg', reply_markup = keyb_client2)
    # await callback_query.message.edit_reply_markup(reply_markup=keyb_client_set)
    if callback_query.data == 'button1':
        await callback_query.message.edit_text(
            'Круто, что ты с нами 🤗 Все уроки по первому начинающему уровню, выбирай урок и присоединяйся ⬇',
            reply_markup=keyb_client_menu)
    elif callback_query.data == 'beginer':
        await callback_query.message.edit_text(
            'Здесь ты найдешь все материалы, которые тебе понадобятся во время обучения.', reply_markup=keyb_client2)
    elif callback_query.data == 'urok1':
        await callback_query.message.edit_text(u1, reply_markup=keyb_client3)
    elif callback_query.data == 'urok2':
        await callback_query.message.edit_text(u2, reply_markup=keyb_client3)
    elif callback_query.data == 'urok3':
        await callback_query.message.edit_text(u3, reply_markup=keyb_client3)
    elif callback_query.data == 'urok4':
        await callback_query.message.edit_text(u4, reply_markup=keyb_client3)
    elif callback_query.data == 'urok5':
        await callback_query.message.edit_text(u5, reply_markup=keyb_client3)
    elif callback_query.data == 'button2':
        await callback_query.message.edit_text('В настройках вы можете поменять язык.', reply_markup=keyb_client_set)
    elif callback_query.data == 'button5':
        await callback_query.message.edit_text(instruction, reply_markup=keyb_client_menu)
    elif callback_query.data == 'back_to_back':
        await callback_query.message.edit_text(
            'Здесь ты найдешь все материалы, которые тебе понадобятся во время обучения.',
            reply_markup=keyb_client_menu)
    elif callback_query.data == 'back':
        await callback_query.message.edit_text('Вы вернулись в главное меню. Выберите раздел.',
                                               reply_markup=keyb_client)
    elif callback_query.data == 'back_to_back01':
        await callback_query.message.edit_text(
            'Здесь ты найдешь все материалы, которые тебе понадобятся во время обучения.', reply_markup=keyb_client2)
    elif callback_query.data == 'beginer1':
        await callback_query.message.edit_text(
            "Прежде чем переходить к первому уровню, рекомендуем ознакомиться с вводным курсом.\n\nЗдесь собраны уроки по учебнику Sejong Korean.",
            reply_markup=keyb_client_level1)
    elif callback_query.data == 'urok_l1':
        await callback_query.message.edit_text("test", reply_markup=keyb_client_level1_back)
    elif callback_query.data == 'urok_l2':
        await callback_query.message.edit_text("test", reply_markup=keyb_client_level1_back)
    elif callback_query.data == 'back_to_back_l1':
        await callback_query.message.edit_text("...", reply_markup=keyb_client_level1)


# Парсер

@dp.message_handler(commands=['get_freshnews_rus'])
async def get_all_news(message: types.Message, parse_mode='HTML'):
    fresh_news = check_news_updates()
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = f"<b>{v['article_time']}</b>\n" \
                   f"{v['article_title']}\n\n" \
                   f"{v['article_url']}\n"

            await message.answer(news, parse_mode='HTML')
    else:
        await message.answer(
            'Свежих новостей пока нет. Попробуйте запустить команду через некоторое время, возможно, новости появятся.')


@dp.message_handler(commands=['get_news_rus'])
async def get_all_news(message: types.Message):
    with open('news_dict.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-3:]:
        news = f"<b>{v['article_time']}</b>\n" \
               f"{v['article_title']}\n\n" \
               f"{v['article_url']}\n"

        await message.answer(news, parse_mode='HTML')

#Хэндлер веб аппа (прикольно, пусть будет так)

@dp.message_handler(commands=['buy'])
async def buy(msg: types.Message):
    button_buy = ReplyKeyboardMarkup(resize_keyboard=True)
    button_buy.add(types.KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url = 'https://replit.com/@AALLEENA/Koreangrandi#index.html')))
    await msg.answer('Ты на странице оплаты курса. Можешь выбрать подходящий и оплатить.', reply_markup=button_buy)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup = on_startup, skip_updates=True)

"""requests.post(f'{url}{bot}/', json={'method': 'SendMessage', 'chat_id': f'{user_id}', 'text': 'something','reply_markup': ['keyboard': [[{'text': 'Yes'}, {'text': 'NO'}]], 'resize_keyboard': True)))"""


### ДОМАШНЕЕ ЗАДАНИЕ НОМЕР 2:
""""

def get_Updates():
    count_message = 0
    while True:
        response = requests.get(f'{url}{TOKEN}/getUpdates').json()
        if count_message != len(response['result']):
            count_message = len(response['result'])
            message = response['result'][-1]
            file_id = message['message']['photo'][-1]['file_id']
            user_id = message['message']['from']['id']
            user_name = message['message']['from']['username']
            requests.get(f'{url}{TOKEN}/sendMessage?chat_id={user_id}&text=Привет,{user_name}.Пришли мне фото, и я отправлю его в ответ.')
            requests.get(f'{url}{TOKEN}/sendPhoto?chat_id={user_id}&photo={file_id}')

get_Updates()
"""

"""with open("sejong.txt", 'rb') as f:

    first_part = f.read(1290)
    second_part = f.readlines()[23::53]
    f.seek(3400)
    third_part = f.read(2338)
    #f.seek()
    #forth_part = f.read(3383)
    #f.seek()
    #fifth_part = f.read(3383)"""


"""""
@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    #await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Круто, что ты с нами 🤗 Все уроки по первому начинающему уровню, выбирай урок и присоединяйся ⬇', reply_markup = keyb_client_menu)

@dp.message_handler(text=['Меню уроков'])
async def hello_message(msg: types.Message):
   await bot.send_message(msg.from_user.id, "Ниже раздел со всеми уроками:", reply_markup = keyb_client2)

@dp.message_handler(text=['Вводный курс'])
async def lesson_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, 'Здесь ты найдешь все материалы, которые тебе понадобятся во время обучения.', reply_markup=keyb_client3)

@dp.callback_query_handler(lambda c: c.data == 'beginer')
async def process_callback_button1(callback_query: types.CallbackQuery):
    #await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text('Здесь ты найдешь все материалы, которые тебе понадобятся во время обучения.', reply_markup = keyb_client2)

@dp.message_handler(text=['🔠Грамматика'])
async def lesson_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, grammar.read(),reply_markup=keyb_client3)

@dp.callback_query_handler(lambda c: c.data == 'button9')
async def settings(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, grammar.read())

#ХЭНДЛЕРЫ ДЛЯ УРОКОВ

@dp.message_handler(text=['Урок 1'])
async def lesson_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, first_part,reply_markup=keyb_client3)

@dp.callback_query_handler(lambda c: c.data == 'urok1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    #await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(f.read(), reply_markup = keyb_client3)
    #await bot.send_message(callback_query.from_user.id, f.read(), reply_markup = keyb_client3)

@dp.message_handler(text=['Урок 2'])
async def lesson_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, second_part,reply_markup=keyb_client3)

@dp.message_handler(text=['Урок 3'])
async def lesson_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, third_part,reply_markup=keyb_client3)
"""""


""""@dp.callback_query_handler(lambda c: c.data == 'back')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Вы вернулись в главное меню. Выберите раздел.', reply_markup = keyb_client)

@dp.message_handler(text=['⚙️Настройки'])
async def lesson_message(msg: types.Message):
   await bot.send_message(msg.from_user.id, '⚙️Настройки', reply_markup=keyb_client_set)


def pulling():
    count_message = 0
    while True:
        response = requests.get(f'{url}{bot}/getUpdates').json()
        if count_message != len(response['result']):
            count_message = len(response['result'])
            message = response['result'][-1]
            file_id = message['message']['photo'][-1]['file_id']
            caption = message['message']['caption']
            user_id = message['message']['from']['id']
            requests.get(f'{url}{bot}/sendPhoto?chat_id={user_id}&photo={file_id}&caption={caption}')
"""

