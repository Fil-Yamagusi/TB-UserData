"""
2023-12-14 @Fil
Телеграм-бот Визитка Александра Сергеевича
Fil FC Визитка Пушкина
fil_fc_pushkin_bot
6886396528:AAHO-KXXB5NS63pKaBAnIIh1wkPrEPd10X8
https://t.me/fil_fc_pushkin_bot
"""

import random
import time

from telebot import TeleBot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, Message
from answers import (get_answers_photo, get_answers_deti,
                     get_answers_dela, get_answers_rhyme,
                     answers_pushkin)


random.seed(time.time())

TOKEN = "6886396528:AAHO-KXXB5NS63pKaBAnIIh1wkPrEPd10X8"
bot = TeleBot(TOKEN)

markup = ReplyKeyboardMarkup(
    row_width=2,
    resize_keyboard=True)
markup.add(* ["❓ Расскажи о себе",
              "🖼 Скинь фотку",
              "✍ Как делишки?",
              "👶 Как детишки?",
              "✴️ Поделись клёвой рифмой?",
              "🆘 ПАМАГИТЕ"])


# Здороваемся, говорим кратко о возможностях бота
@bot.message_handler(
    func=lambda message:
    any(word in message.text.lower()
        for word in ['памаги', 'помоги', 'ыефке', 'руддщ', 'рудз']),
    content_types=["text"])
@bot.message_handler(
    commands=["start", "hello", "help"])
def handle_start(message: Message):
    bot.send_message(
        message.chat.id,
        "Привѣтъ, " +
        message.chat.first_name +
        "! 🤝\nЯ - виртуальный Пушкинъ.\n"
        "Со всѣмъ уваженіемъ къ настоящему!\n\n"
        "Могу немного разсказать о себѣ /about\n"
        "Вот-съ свѣжія дагеротипы изъ салона /photo\n"
        "Новости о дѣлахъ насущныхъ /dela\n"
        "Охотно подѣлюсь новостями о дѣтяхъ /deti\n"
        "Могу подѣлиться знатной риѳмой /rhyme\n\n"
        "Вспомнить cии повелнiя: /help",
        reply_markup=markup
    )


# Краткая биография великого поэта. Спасибо нейросети
@bot.message_handler(
    func=lambda message:
    any(word in message.text.lower()
        for word in ['о себе', 'кто ты']),
    content_types=["text"])
@bot.message_handler(
    commands=["about"])
def handle_about(message: Message):
    for phrase in answers_pushkin:
        bot.send_message(
            message.chat.id,
            phrase,
            parse_mode="HTML",
            reply_markup=markup)


# Оправляем фотку Пушкина
@bot.message_handler(
    func=lambda message:
    any(word in message.text.lower()
        for word in ['фото', 'фотк', 'картин']),
    content_types=["text"])
@bot.message_handler(commands=["photo"])
def handle_photo(message: Message):
    with open(f"photo/{random.randint(1, 25)}.webp", 'rb') as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=get_answers_photo(),
            reply_markup=markup
        )


# Случайная новость о делах Пушкина. Подгружается из списка во внешнем файле
@bot.message_handler(
    func=lambda message:
    any(word in message.text.lower()
        for word in ['дела', 'делиш', 'вудф']),
    content_types=["text"])
@bot.message_handler(commands=["dela"])
def handle_dela(message: Message):
    bot.send_message(
        message.chat.id,
        get_answers_dela() +
        "\n\n<i>За творческие новости спасибо нейросети.</i>",
        parse_mode="HTML",
        reply_markup=markup)


# Случайный факт о детях Пушкина. Подгружается из списка во внешнем файле
@bot.message_handler(
    func=lambda message:
    any(word in message.text.lower()
        for word in ['дети', 'детя', 'детк', 'вуеш']),
    content_types=["text"])
@bot.message_handler(commands=["deti"])
def handle_deti(message: Message):
    bot.send_message(
        message.chat.id,
        get_answers_deti() +
        "\n\n<i>Кстати, это факты от нейросети! Ошибка на ошибке!</i>",
        parse_mode="HTML",
        reply_markup=markup)


# Случайная прикольная рифма. Подгружается из списка во внешнем файле
@bot.message_handler(
    func=lambda message:
    any(word in message.text.lower()
        for word in ['рифм', 'зарифм', 'крнь']),
    content_types=["text"])
@bot.message_handler(commands=["rhyme"])
def handle_rhyme(message: Message):
    bot.send_message(
        message.chat.id,
        get_answers_rhyme(),
        parse_mode="HTML",
        reply_markup=markup)


# Для наставника
@bot.message_handler(commands=["description"])
def handle_description(message: Message):
    bot.send_message(
        message.chat.id,
        "Кроме команд, бот ответит и на сообщения. Например:\n"
        "/start = /hello = /help = "
        "['памаги', 'помоги', 'ыефке', 'руддщ', 'рудз']\n"
        "/about = ['о себе', 'кто ты']\n"
        "/photo = ['фото', 'фотк', 'картин']\n"
        "/dela = ['дела', 'делиш', 'вудф']\n"
        "/deti = ['дети', 'детя', 'детк', 'вуеш']\n"
        "/rhyme = ['рифм', 'зарифм', 'крнь']\n\n"
        "Бот может показать не тот раздел, если несколько ключевых слов найдёт"
        " во фразе, зато на словоформы и простые опечатки старается ответить:\n"
        "<i>зарифмуй чё-нить?</i>\n"
        "<i>что делаешь?</i>\n"
        "<i>расскажи о семье, о детях?</i>\n",
        parse_mode="HTML",
        reply_markup=markup)


print(TOKEN)
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        time.sleep(5)
