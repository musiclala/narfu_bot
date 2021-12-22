import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import locale

URL_NARFU = 'https://ruz.narfu.ru/'

# Настриваем дату и получаем в таком виде, как на сайте сафу
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
date = datetime.today().strftime('%d.%m.%Y')


def get_urls_list_high_schools():
    """
    Получаем список ссылок всех высших школ для получения всех номеров групп и их ссылок на детальное расписание
    :return: <list> 'urls_list_high_school'
    """
    response_narfu = requests.get(URL_NARFU)
    response_narfu.encoding = 'utf-8'
    soup_for_high_school = BeautifulSoup(response_narfu.text, 'lxml')

    # получаем список высших школ
    find_name_high_school = soup_for_high_school.find_all('div', id='classic')

    url_high_school = ''
    for i in find_name_high_school:
        url_high_school = i.find_all('div', class_='visible-xs col-xs-12 institution_button xs')

    urls_list_high_school = {}
    for i in url_high_school:
        urls_list_high_school[i.find('a')['href'].partition('=')[2]] = [i.text.strip(), URL_NARFU + i.find('a')['href']]

    return urls_list_high_school


# print(get_urls_list_high_schools())


def get_url_number_group(number_high_school: int):
    """
    Получаем словарь всех номеров групп и их ссылок на детальное расписание
    Количество групп на 02.12.21 - 728
    :return: <dict> 'number_groups_url'

    Попробовать реализовать словарь {Номер высшей школы: {номер группы: ссылка}}
    """
    url_hs = ''
    dictonary = get_urls_list_high_schools()
    for i in dictonary:
        if i == str(number_high_school):
            url_hs = dictonary[i][1]

    number_groups_url = {}
    # Проходим по всем высшим школам и собираем все группы
    # for url_hs in get_urls_list_high_schools():

    response_groups = requests.get(url_hs)
    soup_for_number_groups = BeautifulSoup(response_groups.text, 'lxml')

    # Ищем ссылки на детальное расписание каждой группы
    find_number_group = soup_for_number_groups.find_all('a', class_='visible-xs')

    # Сохраняем номера групп и ссылки
    for num_gr in find_number_group:
        number_groups_url[num_gr.find('span').text] = URL_NARFU + num_gr['href']

    return number_groups_url


# print(get_url_number_group(15))


def find_url_for_group(number_group):
    spisok = get_url_number_group(15)
    if str(number_group) in spisok.keys():
        return spisok[str(number_group)]
    else:
        return "Данная группа обучается не в этой высшей школе! Выберите другую"


# print(find_url_for_group(122111))


def find_date():
    response_date = requests.get(find_url_for_group(122111))
    response_date.encoding = 'utf-8'
    soup_for_date = BeautifulSoup(response_date.text, 'lxml')

    find_date = soup_for_date.find_all('div', class_='dayofweek')

    dict_date = {}
    for i in find_date:
        date_on_site = re.sub("^\s+|\n|\r|\s|\s+$", '', i.text)
        if date_on_site.partition(',')[2] >= date.strip():
            dict_date[date_on_site] = '-'.join(i.parent['class'])
    return dict_date


print(find_date())


def find_detail_schedule(date_for_schedule):
    dict_date = find_date()
    lol = ''
    for i in dict_date:
        if i == date_for_schedule:
            lol = dict_date.items()!

    response_schedule = requests.get(find_url_for_group(122111))
    response_schedule.encoding = 'utf-8'
    soup_for_schedule = BeautifulSoup(response_schedule.text, 'lxml')

    return lol


print(find_detail_schedule('суббота,17.12.21'))
print(date)
