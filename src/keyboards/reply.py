from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text="📝 Расписание"),
            KeyboardButton(text="📍 Выбрать группу"),
            KeyboardButton(text="👨‍🎓 Профиль"),
        ],
        [
            KeyboardButton(text="🔄 Обновить"),
        ],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        input_field_placeholder="Выберите действие из меню",
        selective=True,
        resize_keyboard=True,
    )
