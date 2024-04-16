import asyncio

from src.props.dicts import WEEKDAY_DICT, INTERVAL_DICT, LESSON_TYPE
from src.utils.parsing import get_group_schedule
import datetime


async def get_schedule(group: str, date: str) -> str:
    schedule = await get_group_schedule(group)
    result = f"Расписание для группы ({group}):\n"
    start, end = map(
        lambda day: datetime.datetime.strptime(day, "%Y-%m-%d"), date.split(":")
    )

    current_day = start
    # Цикл по датам
    while current_day <= end:
        if "classes" not in schedule:
            return result
        for lesson in schedule["classes"]:
            if current_day.strftime("%Y-%m-%d") in lesson["dates"]:
                result += (
                    f"=" * 20 + "\n"
                    f"🗓 День {WEEKDAY_DICT[lesson['day']]}, Неделя {lesson['week']}:\n"
                    f"🕘 Время занятия: ({INTERVAL_DICT[str(lesson['class'])]['start']} - {INTERVAL_DICT[str(lesson['class'])]['end']})\n"
                    f"🏫 Аудитория: {lesson['auditorium']}\n"
                    f"👨‍🏫 Преподаватель: {lesson['lecturer']}\n"
                    f"📚 Дисциплина: {lesson['discipline']}\n"
                    f"📝 Тип занятия: {LESSON_TYPE[lesson['type']]['name']}\n"
                )

        current_day += datetime.timedelta(days=1)
    return result


async def get_week(current: bool = True) -> str:
    # текущая дата
    now = datetime.datetime.now()

    # количество дней, прошедших после понедельника (0 = понедельник)
    delta_days = now.weekday()

    # дата понедельника
    monday = (
        now
        - datetime.timedelta(days=delta_days)
        + (datetime.timedelta(days=7) if current else datetime.timedelta(days=0))
    )
    # дата субботы
    saturday = (
        now
        + datetime.timedelta(days=6 - delta_days)
        + (datetime.timedelta(days=7) if current else datetime.timedelta(days=0))
    )
    return monday.strftime("%Y-%m-%d") + ":" + saturday.strftime("%Y-%m-%d")


if __name__ == "__main__":
    # print((datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
    asyncio.run(get_schedule("010304-КМСа-о23", "2024-04-15:2024-04-15"))
