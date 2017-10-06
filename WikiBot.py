#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from config import TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

pages = {
    'roles': """
*ВИДЫ ПЕРСОНАЖЕЙ, ИХ ЦЕЛИ И ВОЗМОЖНОСТИ:*
*1. Журналист*
_Задача:_ публиковать новости, собрать капитал. 
Есть возможность продавать информацию разработчикам и нуждающимся.
*2. Полисмен*
_Задача:_ поймать как можно больше разорителей. 
Есть возможность созывать присяжных для суда и запросить историю игрока.
*3. Разорители*
_Задача:_ слить как можно больше денег(собрать отрицательный капитал). Возможность выступать на суде одновременно и подсудимым и адвокатом.
*4.  Мирные*
_Задача:_ собрать капитал. Есть возможность подать прошение(платно) на рассмотрение дела по подозрению определенного человека в разорении. 
*5.  Разработчик*
_Задача:_ сделать годный проект. Собрать капитал, найти спонсоров и покупателей.
*6.  Спонсоры*
_Задача:_ максимизировать число удачных инвестиций; собрать капитал. 
(Инвестиция считается удачной, если выручка превзошла вложения в проект. Доля спонсора обговаривается с разработчиками.)
    """,

    'money': """ 
*Способы получения денег*
1.  Собрать разбросанную валюту по центру
2.  Вложить деньги в удачный проект и получить прибыль
3.  Искать подработку на стороне, помогая различным персонажам
4.  Найти ящик Пандоры
    """,

    'victory': """ 
*Виды победы*
1. Собрать наибольший капитал
2. Сделать лучшего бота
3. Сделать наибольшее количество удачных инвестиций
4. Выполнить наибольшее количество задач
    """,

    'news': """
*Новости:*
1. *День независимости!*
День независимости произошел в Берляндии 6 октября 2017 года. 
При голосовании мнения разделились, но большее количество было за объявлении 
Берляндии независимой страной. Блгодаря этому, 6 октября и стало памятной датой в нашей стране.
2. Смирнов Игорь был пойман на денежном мошенничестве
Слухи утверждают, что Смирнов Игорь Андреевич переводил отрицательные суммы неизвестным личностям! 
Подозреваемый пытался оправдаться, но полиция была неуклонна. 
Кажется, скоро будет зазываться совет присяжных. 
3. Также полиция подозревает в мошенничестве Мирскова Андрея. Информация не подверждена
4. Неожиданные новости. Противники признания независимости Берляндии осадили здание правительства! 
Объявляется всеобщая воинская повинность!
""",
    'ads': """
*ВАША РЕКЛАМА*
Всего 10K - и ваша реклама будет тут :)
"""
}


def menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "Виды персонажей их цели и возможности",
                callback_data='roles'
            ),
            InlineKeyboardButton(
                "Способы получения денег в игре",
                callback_data='money'
            )
        ],
        [
            InlineKeyboardButton(
                "Виды победы",
                callback_data='victory'
            ),
            InlineKeyboardButton(
                "Новости Берляндии",
                callback_data='news'
            ),
            InlineKeyboardButton(
                "РЕКЛАМА",
                callback_data='ads'
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def start(bot, update):
    update.message.reply_text('Wiki-bot по ролевой игре Берляндия, центр Интеллект',
                              reply_markup=menu())


def button(bot, update):
    query = update.callback_query
    key = query.data
    text = "Страница: %s" % key
    if key in pages:
        text = pages[key]

    bot.edit_message_text(
        text=text, parse_mode="Markdown",
        reply_markup=menu(),
        chat_id=query.message.chat_id,
        message_id=query.message.message_id
    )


def help(bot, update):
    update.message.reply_text("Команда /start для запуска бота")


def error(bot, update, error):
    logging.warning('Команда "%s" вызвала ошибку "%s"' % (update, error))


# Create the Updater and pass it your bot's token.
updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_error_handler(error)

# Start the Bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()
