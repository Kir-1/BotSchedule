from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.fsm.main_state import MainState
from src.keyboards.inline import get_choose_keyboard, get_schedule_menu_keyboard
from src.keyboards.reply import get_main_menu_keyboard
from src.texts.users import (
    get_choose_text,
    get_wait_text,
    get_user_profile,
    get_user_refresh,
)
from src.utils.parsing import get_dict_faculty
from src.fsm.wait_state import WaitState
from src.fsm.fsm import FSM

router = Router(name=__name__)


@router.message(F.text == "📍 Выбрать группу", MainState.main)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """Обработчик выбора группы"""
    async with FSM(state_context=state, state=WaitState.wait) as state:
        faculties = list((await get_dict_faculty()).keys())
        await message.bot.send_message(
            message.from_user.id,
            await get_choose_text("факультет"),
            reply_markup=await get_choose_keyboard("факультет", faculties),
        ),


@router.message(F.text == "📝 Расписание", MainState.main)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """Обработчик выбора даты для расписания"""
    data = await state.get_data()

    if not all([data.get("faculty", None), data.get("group", None)]):
        await message.answer("Вы должны указать группу")
        return

    async with FSM(state_context=state, state=WaitState.wait) as state:

        await message.bot.send_message(
            chat_id=message.chat.id,
            text=await get_choose_text("дату"),
            reply_markup=await get_schedule_menu_keyboard(),
        )


@router.message(F.text == "👨‍🎓 Профиль", MainState.main)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """Обработчик профиля"""
    data = await state.get_data()

    async with FSM(state_context=state, state=WaitState.wait) as state:

        await message.bot.send_message(
            chat_id=message.chat.id,
            text=await get_user_profile(
                data.get("faculty", None), data.get("group", None)
            ),
        )


@router.message(F.text == "🔄 Обновить")
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """Обработчик обновления"""

    await message.answer(
        await get_user_refresh(),
        reply_markup=await get_main_menu_keyboard(),
    )

    await state.update_data(faculty=None, group=None)
    await state.set_state(MainState.main)
