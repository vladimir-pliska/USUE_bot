# -*- coding: utf-8 -*-

import telebot
import datetime
from keyboard_markups import Keyboard

from important_parameters import token
from database_and_parsing import UserPosition, Subscription, get_groups, group_list, load_schedule_page


bot = telebot.TeleBot(token)
keyboard = Keyboard(bot)
get_groups()


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


@bot.message_handler(func=lambda mess: u"Главное меню" == mess.text,
                     content_types=["text"])
def handle_text(message):
    keyboard.main_menu(message)


@bot.message_handler(func=lambda mess: u"Получить расписание" == mess.text, content_types=["text"])
def handle_text(message):
    UserPosition.set_starting_position(str(message.from_user.id), message.from_user.username)
    keyboard.get_faculties(message)


@bot.message_handler(func=lambda mess: u"Магистратуры" == mess.text, content_types=["text"])
def handle_text(message):
    UserPosition.set_faculty_position(str(message.from_user.id), message.text)
    keyboard.two_courses(message)


@bot.message_handler(func=lambda mess: u"ИНО (ФСП)" == mess.text or u"ИДО" == mess.text, content_types=["text"])
def handle_text(message):
    UserPosition.set_faculty_position(str(message.from_user.id), message.text)
    keyboard.three_courses(message)


@bot.message_handler(func=lambda mess: u"Менеджмента и информационных технологий" == mess.text or
                     u"Торговли, пищевых технологий и сервиса" == mess.text or u"Финансов и права" == mess.text or
                     u"Экономики" == mess.text or u"Заочного обучения" == mess.text, content_types=["text"])
def handle_text(message):
    UserPosition.set_faculty_position(str(message.from_user.id), message.text)
    keyboard.four_courses(message)


@bot.message_handler(func=lambda mess: u"1 курс" == mess.text or u"2 курс" == mess.text or u"3 курс" == mess.text or
                                       u"4 курс" == mess.text, content_types=["text"])
def handle_text(message):
    UserPosition.set_course_position(str(message.from_user.id), message.text[:1])
    faculty, course = UserPosition.get_faculty_and_course(str(message.from_user.id))
    groups = UserPosition.get_groups(faculty, course)
    groups.sort()
    keyboard.form_group_list(message, groups)


@bot.message_handler(func=lambda mess: mess.text in group_list, content_types=["text"])
def handle_text(message):
    UserPosition.set_group_position(str(message.from_user.id), message.text)
    keyboard.schedule_menu(message)


@bot.message_handler(func=lambda mess: u"Подписаться на эту группу" == mess.text,
                     content_types=["text"])
def handle_text(message):
    group = UserPosition.get_chosen_group(str(message.from_user.id))
    Subscription.set_subscription(str(message.from_user.id), group)
    bot.send_message(message.chat.id, u'Вы подписались на группу {0}.'.format(group))


@bot.message_handler(func=lambda mess: u"На сегодня" == mess.text or u"На завтра" == mess.text, content_types=["text"])
def handle_text(message):
    today = datetime.datetime.today()
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    weekday_today = today.weekday()
    weekday_tomorrow = tomorrow.weekday()

    group = UserPosition.get_chosen_group(str(message.from_user.id))

    if message.text == u"На сегодня":
        if weekday_today == 6:
            bot.send_message(message.chat.id, "Сегодня выходной день!")
        else:
            bot.send_message(message.chat.id, "Расписание на сегодня *({0})*:".format(today.strftime("%d.%m.%Y")[:5]),
                             parse_mode="Markdown")
            bot.send_message(message.chat.id, UserPosition.get_schedule(group, today))
    else:
        if weekday_tomorrow == 6:
            bot.send_message(message.chat.id, "Завтра выходной день!")
        else:
            bot.send_message(message.chat.id, "Расписание на завтра *({0})*:".format(tomorrow.strftime("%d.%m.%Y")[:5]),
                             parse_mode=["Markdown"])
            bot.send_message(message.chat.id, UserPosition.get_schedule(group, tomorrow))


@bot.message_handler(func=lambda mess: u"Расписание по подписке" == mess.text, content_types=["text"])
def handle_text(message):
    today = datetime.datetime.today()
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    weekday_today = today.weekday()
    weekday_tomorrow = tomorrow.weekday()

    group = Subscription.get_subs_group(str(message.from_user.id))

    if Subscription.is_subscriber(str(message.from_user.id)):
        bot.send_message(message.chat.id, "Вы подписаны на группу *" + group.encode('utf-8') + "*.",
                         parse_mode="Markdown")
        if weekday_today == 6:
            bot.send_message(message.chat.id, "Сегодня выходной день!")
        else:
            bot.send_message(message.chat.id, "Расписание на сегодня *({0})*:".format(today.strftime("%d.%m.%Y")[:5]),
                             parse_mode="Markdown")
            bot.send_message(message.chat.id, UserPosition.get_schedule(group, today))

        if weekday_tomorrow == 6:
            bot.send_message(message.chat.id, "Завтра выходной день!")
        else:
            bot.send_message(message.chat.id, "Расписание на завтра *({0})*:".format(tomorrow.strftime("%d.%m.%Y")[:5]),
                             parse_mode=["Markdown"])
            bot.send_message(message.chat.id, UserPosition.get_schedule(group, tomorrow))
    else:
        bot.send_message(message.chat.id, "К сожалению, вы не подписаны ни на одну группу.")


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


@bot.message_handler(func=lambda mess: u"Вернуться назад" == mess.text, content_types=["text"])
def handle_text(message):
    user_position = UserPosition.get_user_position(str(message.from_user.id))
    faculty, course = UserPosition.get_faculty_and_course(str(message.from_user.id))

    if user_position == 3:
        UserPosition.cancel_starting_position(str(message.from_user.id))
        keyboard.main_menu(message)

    if user_position == 2:
        UserPosition.cancel_faculty(str(message.from_user.id))
        keyboard.get_faculties(message)

    if user_position == 1:
        UserPosition.cancel_course(str(message.from_user.id))

        if faculty == u"Магистратуры":
            keyboard.two_courses(message)

        if faculty == u"ИНО (ФСП)" or faculty == u"ИДО":
            keyboard.three_courses(message)

        if (faculty == u"Менеджмента и информационных технологий" or
                faculty == u"Торговли, пищевых технологий и сервиса" or
                faculty == u"Финансов и права" or faculty == u"Экономики" or faculty == u"Заочного обучения"):
            keyboard.four_courses(message)

    if user_position == 0:
        UserPosition.cancel_group(str(message.from_user.id))
        groups = UserPosition.get_groups(faculty, course)
        groups.sort()
        keyboard.form_group_list(message, groups)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.from_user.id, "I'm sorry, " + message.from_user.first_name +
                     ", there's not much I can do yet...")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.from_user.id, "Такому пока не научены ¯\_(ツ)_/¯")

bot.polling()
