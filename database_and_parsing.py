# -*- coding: utf-8 -*-

import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient, DESCENDING
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from additional_data import schedule_url

client = MongoClient("localhost", 27017)
db = client.schedule
group_list = []


def get_groups():
    cursor = db.groups.find()

    for group in cursor:
        group_list.append(group["name"])

    cursor.close()


def load_schedule_page():
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)

    driver = webdriver.Chrome()
    driver.get(schedule_url)

    db.schedule.remove({})

    try:
        """
        Работает жопой, нужно разбираться
        """
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "main"))
        )
    finally:
        driver.refresh()

    for group in group_list:
        driver.find_element_by_id("searchClient").clear()
        driver.find_element_by_id("searchClient").send_keys(group)

        driver.find_element_by_id("DATK").clear()
        driver.find_element_by_id("DATK").send_keys(tomorrow.strftime("%d.%m.%Y"))

        driver.find_element_by_id("DATN").clear()
        driver.find_element_by_id("DATN").send_keys(today.strftime("%d.%m.%Y"))

        driver.find_element_by_xpath("//input[@type='button' and @value='Показать расписание']").click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        schedule_table = soup.find("table", {"id": "main"})

        parse_schedule(group, schedule_table, today, tomorrow)

    driver.close()


def parse_schedule(group, table, today, tomorrow):
    i = 0

    for tr in table("tr"):
        row_class = tr.attrs.get("class")

        if row_class is not None:
            if "zag" in row_class or "rowdate" in row_class:
                tr.extract()
                continue

        cells = tr.findAll("td")

        if i < 8:
            date = today.strftime("%d.%m.%Y")
        else:
            date = tomorrow.strftime("%d.%m.%Y")

        try:
            if cells[2].text != "":
                number = cells[0].text
                subject = cells[2].text
                teacher = cells[3].text
                classroom = cells[4].text

                db.schedule.insert({"date": date,
                                    "group": group,
                                    "num": number,
                                    "subject": subject,
                                    "teacher": teacher,
                                    "classroom": classroom})

            i += 1
        except LookupError:
            continue


class UserPosition:
    def __init__(self):
        print("yay")

    @staticmethod
    def set_starting_position(user_id, username):
        db.user_log.insert({"chat_id": user_id,
                            "username": username,
                            "faculty": "empty",
                            "course": "empty",
                            "group": "empty"})

    @staticmethod
    def set_faculty_position(user_id, faculty_name):
        db.user_log.find_one_and_update({"chat_id": user_id},
                                        {"$set": {"faculty": faculty_name}},
                                        sort=[("_id", DESCENDING)])

    @staticmethod
    def set_course_position(user_id, course):
        db.user_log.find_one_and_update({"chat_id": user_id},
                                        {"$set": {"course": course}},
                                        sort=[("_id", DESCENDING)])

    @staticmethod
    def set_group_position(user_id, group):
        db.user_log.find_one_and_update({"chat_id": user_id},
                                        {"$set": {"group": group}},
                                        sort=[("_id", DESCENDING)])

    @staticmethod
    def get_faculty_and_course(user_id):
        cursor = db.user_log.find({"chat_id": user_id})
        for entry in cursor:
            faculty = entry["faculty"]
            course = entry["course"]

        return faculty, course

    @staticmethod
    def get_groups(faculty, course):
        to_return = []

        cursor = db.groups.find({"faculty": faculty,
                                 "course": int(course)})
        for group in cursor:
            to_return.append(group["name"])

        return to_return

    @staticmethod
    def get_schedule(group):
        return 0

    @staticmethod
    def get_user_position(user_id):
        cursor = db.user_log.find({"chat_id": user_id})
        for entry in cursor:
            count = 0

            for key, value in entry.iteritems():
                if value == "empty":
                    count += 1

        return count

    @staticmethod
    def cancel_starting_position(user_id):
        db.user_log.find_one_and_delete({"chat_id": user_id},
                                        sort=[("_id", DESCENDING)])

    @staticmethod
    def cancel_faculty(user_id):
        db.user_log.find_one_and_update({"chat_id": user_id},
                                        {"$set": {"faculty": "empty"}},
                                        sort=[("_id", DESCENDING)])

    @staticmethod
    def cancel_course(user_id):
        db.user_log.find_one_and_update({"chat_id": user_id},
                                        {"$set": {"course": "empty"}},
                                        sort=[("_id", DESCENDING)])

    @staticmethod
    def cancel_group(user_id):
        db.user_log.find_one_and_update({"chat_id": user_id},
                                        {"$set": {"group": "empty"}},
                                        sort=[("_id", DESCENDING)])
