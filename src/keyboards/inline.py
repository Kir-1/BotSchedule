import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.utils.schedule import get_week


async def get_choose_keyboard(title: str, target: list[str]):
    keyboard = []

    for element, index in zip(target, range(len(target))):
        keyboard.append(
            [InlineKeyboardButton(text=element, callback_data=f"{title} {index}")]
        )

    keyboard.append(
        [InlineKeyboardButton(text="⬅назад", callback_data=f"назад {title}")]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_schedule_menu_keyboard() -> InlineKeyboardMarkup:
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    tomorrow = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime(
        "%Y-%m-%d"
    )
    keyboard = [
        [
            InlineKeyboardButton(
                text="⏺ Расписание на сегодня",
                callback_data=f"расписание группы {today}:{today}",
            ),
            InlineKeyboardButton(
                text="⏹ Расписание на завтра",
                callback_data=f"расписание группы {tomorrow}:{tomorrow}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🔼 Расписание на неделю",
                callback_data=f"расписание группы {await get_week(current=True)}",
            ),
            InlineKeyboardButton(
                text="🔼 Расписание на следующую неделю",
                callback_data=f"расписание группы {await get_week(current=False)}",
            ),
        ],
        [InlineKeyboardButton(text="⬅назад", callback_data=f"назад дата")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_back_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="⬅назад", callback_data=f"назад меню")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
