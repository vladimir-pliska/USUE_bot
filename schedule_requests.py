# -*- coding: utf-8 -*-

import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from additional_data import schedule_url, group_list
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def load_page():
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)

    driver = webdriver.Chrome()
    driver.get(schedule_url)

    try:
        element = WebDriverWait(driver, 5).until(
            EC.title_is(u"Расписание УрГЭУ")
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

        parse_schedule(schedule_table, today, tomorrow)

    driver.close()


def parse_schedule(table, today, tomorrow):
    today.strftime("%d.%m.%Y")  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    tomorrow.strftime("%d.%m.%Y")  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    i = 0

    for tr in table("tr"):
        row_class = tr.attrs.get("class")

        if row_class is not None:
            if 'zag' in row_class or 'rowdate' in row_class:
                tr.extract()
                continue

        cells = tr.findAll("td")

        if i < 8:
            date = today.strftime("%d.%m.%Y")
        else:
            date = tomorrow.strftime("%d.%m.%Y")

        if cells[2].text != "":
            number = cells[0].text
            subject = cells[2].text
            teacher = cells[3].text
            classroom = cells[4].text
            # тут будет вызываться команда записи пары в бд со всеми этими данными, но пока выводим в консоль
            print(date + " - " + number + " - " + subject + " - " + teacher + " - " + classroom)

        i += 1


load_page()
