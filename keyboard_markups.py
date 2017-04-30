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
        user_markup.row("Обновления", "Обратная связь")

        self.bot.send_message(message.from_user.id, "Выберите пункт меню:", reply_markup=user_markup)

    def get_faculties(self, message):
        faculty_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        faculty_markup.row("Вернуться назад")
        for faculty in faculty_list:
            faculty_markup.row(faculty)

        self.bot.send_message(message.from_user.id, "Выберите институт:", reply_markup=faculty_markup)
