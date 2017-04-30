# -*- coding: utf-8 -*-

import telebot
from keyboard_markups import Keyboard
from important_parameters import token


bot = telebot.TeleBot(token)
keyboard = Keyboard(bot)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("Chat initialized with user " + message.from_user.username + ", chat ID: " + str(message.from_user.id))

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("Получить расписание")
    user_markup.row("Расписание по подписке")
    user_markup.row("Время пар/перерывов")
    user_markup.row("Обратная связь")

    bot.send_message(message.from_user.id, u"Добро пожаловать, " + message.from_user.first_name + "!")
    bot.send_message(message.from_user.id, "Выберите пункт меню:", reply_markup=user_markup)


@bot.message_handler(func=lambda mess: u"Главное меню" == mess.text, content_types=["text"])
def handle_text(message):
    keyboard.main_menu(message)


@bot.message_handler(func=lambda mess: u"Получить расписание" == mess.text, content_types=["text"])
def handle_text(message):
    keyboard.get_faculties(message)


@bot.message_handler(func=lambda mess: u"Расписание по подписке" == mess.text, content_types=["text"])
def handle_text(message):
    bot.send_message(message.from_user.id, "Вы нажали на кнопку 'Расписание по подписке'! Здесь потом что-нибудь будет")


@bot.message_handler(func=lambda mess: u"Время пар/перерывов" == mess.text, content_types=["text"])
def handle_text(message):
    bot.send_message(message.from_user.id, "*Институты Менеджмента и информационных технологий, Финансов и права, "
                                           "Экономики:*\n"
                                           "*1 пара:* 8:30 - 10:00\n*2 пара:* 10:10 - 11:40\n*3 пара:* 11:50 - 13:20\n"
                                           "*4 пара:* 13:50 - 15:20\n*5 пара:* 15:30 - 17:00\n*6 пара:* 17:10 - 18:40\n"
                                           "*7 пара:* 18:50 - 20:20\n*8 пара:* 20:30 - 22:00", parse_mode="Markdown")

    bot.send_message(message.from_user.id, "*Институт Торговли, пищевых технологий и сервиса:*\n"
                                           "*1 пара:* 8:30 - 10:00\n*2 пара:* 10:10 - 11:40\n*3 пара:* 12:10 - 13:40\n"
                                           "*4 пара:* 13:50 - 15:20\n*5 пара:* 15:30 - 17:00\n*6 пара:* 17:10 - 18:40\n"
                                           "*7 пара:* 18:50 - 20:20\n*8 пара:* 20:30 - 22:00", parse_mode="Markdown")


@bot.message_handler(func=lambda mess: u"Обратная связь" == mess.text, content_types=["text"])
def handle_text(message):
    bot.send_message(message.from_user.id, "Вопросы, предложения и замечания:\n • @Tommy_Jacket\n • "
                                           "mr.tommyjacket@gmail.com")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "I'm sorry, " + message.from_user.first_name +
                     ", there's not much I can do yet...")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.from_user.id, "А тут все остальное пока =)")

bot.polling()
