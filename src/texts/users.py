async def get_choose_text(title: str) -> str:
    text = f"☑ Выберите {title}: "
    return text


async def get_wait_text() -> str:
    text = (
        "☝️Бот сейчас занят 🔄 обработкой вашего запроса... 🤖 Пожалуйста, ожидайте немного... ⏳ 🌟"
        " Спасибо за терпение! 💫"
    )
    return text


async def get_user_profile(faculty: str | None, group: str | None) -> str:

    text = f"🏛 Факультет: {faculty}\n👥 Группа: {group}"

    return text


async def get_user_refresh() -> str:
    text = "Все данные были обновлены"
    return text
