# -*- coding: utf-8 -*-

import telebot

from additional_data import faculty_list


class Keyboard:
    def __init__(self, bot):
        self.bot = bot

    def main_menu(self, message):
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Получить расписание")
        user_markup.row("Расписание по подписке")
        user_markup.row("Время пар/перерывов")
        user_markup.row("Обратная связь")

        self.bot.send_message(message.from_user.id, "Выберите пункт меню:", reply_markup=user_markup)

    def get_faculties(self, message):
        faculty_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        faculty_markup.row("Вернуться назад")
        for faculty in faculty_list:
            faculty_markup.row(faculty)

        self.bot.send_message(message.from_user.id, "Выберите институт:", reply_markup=faculty_markup)

    def two_courses(self, message):
        course_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        course_markup.row("Вернуться назад")
        course_markup.row("1 курс", "2 курс")

        self.bot.send_message(message.from_user.id, "Выберите курс:", reply_markup=course_markup)

    def three_courses(self, message):
        course_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        course_markup.row("Вернуться назад")
        course_markup.row("1 курс", "2 курс")
        course_markup.row("3 курс")

        self.bot.send_message(message.from_user.id, "Выберите курс:", reply_markup=course_markup)

    def four_courses(self, message):
        course_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        course_markup.row("Вернуться назад")
        course_markup.row("1 курс", "2 курс")
        course_markup.row("3 курс", "4 курс")

        self.bot.send_message(message.from_user.id, "Выберите курс:", reply_markup=course_markup)

    def form_group_list(self, message, groups):
        list_length = len(groups)

        group_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        group_markup.row("Вернуться назад")
        if list_length > 0:
            for i in range(0, list_length, 2):
                if i + 1 == list_length:
                    group_markup.row(groups[i])
                    break
                group_markup.row(groups[i], groups[i + 1])

        self.bot.send_message(message.from_user.id, 'Выберите группу:', reply_markup=group_markup)

    def schedule_menu(self, message):
        menu_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        menu_markup.row("На сегодня", "На завтра")
        menu_markup.row("Подписаться на эту группу (и поставить лайк)")
        menu_markup.row("Главное меню", "Вернуться назад")

        self.bot.send_message(message.from_user.id, "Выберите пункт меню:", reply_markup=menu_markup)
