# импорт библиотек
import asyncio
import json

import requests
from bs4 import BeautifulSoup
from src.props.urls import (
    FACULTY_URL,
    GROUP_URL,
    GROUP_SCHEDULE_BASE_INFO_URL,
    GROUP_SCHEDULE_URL,
)
from src.props.dicts import FACULTY_DICT


async def get_dict_faculty() -> dict:
    """Данная функция возвращает словарь факультетов с группами"""

    faculty_dict = {}

    # получение HTML страницы факультетов
    response = requests.get(FACULTY_URL)
    # проверка статуса ответа
    if response.status_code != 200:
        return FACULTY_DICT

    # применение BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, "html.parser")

    for link in soup.findAll("a"):
        href = link.get("href")
        if href.startswith("uTT_Grup1.php"):
            parameters = href.split("?")[1].split("&")
            faculty_dict[parameters[1].split("=")[1]] = await get_list_groups(
                url=GROUP_URL,
                params={
                    "KFak": parameters[0].split("=")[1],
                    "NameF": parameters[1].split("=")[1],
                    "kurs": "1",
                },
            )
    return faculty_dict


async def get_list_groups(url: str, params: dict) -> list:
    """Данная функция возвращает список групп"""

    # получение HTML страницы групп
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return FACULTY_DICT[params["NameF"]]
    soup = BeautifulSoup(response.text, "html.parser")
    group_list = []

    # найдем все элементы <a> на страницы
    for link in soup.find_all("a"):
        # проверим, содержит ли href нужные параметры
        if "GRUPPA" in link.get("href", ""):
            # извлекаем и очищаем значение GRUPPA
            grp = link["href"].split("GRUPPA=")[1].split("&")[0].split("<")[0]
            group_list.append(grp)

    return group_list


async def get_group_schedule(group: str) -> dict:
    """Данная функция возвращает расписание группы"""

    # получаем основную информацию о группе факультет, год обучение и т.д
    response = requests.get(GROUP_SCHEDULE_BASE_INFO_URL.format(group=group))
    if response.status_code != 200:
        return {}

    # получаем расписание
    response = requests.get(GROUP_SCHEDULE_URL.format(**response.json()[group]))

    # в случае успешного запроса, статус код будет 200
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return {}


if __name__ == "__main__":
    # asyncio.run(get_dict_faculty())
    asyncio.run(get_group_schedule("010304-КМСа-о23"))
