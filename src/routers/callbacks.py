from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.fsm.fsm import FSM
from src.fsm.main_state import MainState
from src.fsm.wait_state import WaitState
from src.texts.users import get_choose_text
from src.keyboards.inline import (
    get_choose_keyboard,
    get_schedule_menu_keyboard,
    get_back_keyboard,
)
from src.utils.parsing import get_dict_faculty
from src.utils.schedule import get_schedule

router = Router(name=__name__)


@router.callback_query(WaitState.wait)
async def callback_wait_handler(callback_query: CallbackQuery):
    await callback_query.answer("⏳ Пожалуйста подождите")


@router.callback_query(F.data.startswith("назад"), MainState.main)
async def callback_back_handler(callback_query: CallbackQuery, state: FSMContext):
    """Обработчик шага назад в меню"""

    async with FSM(state_context=state, state=WaitState.wait) as state:
        if callback_query.data.split(" ")[1] == "факультет":
            await state.update_data(faculty=None)
            await callback_query.message.delete()
        elif callback_query.data.split(" ")[1] == "группа":
            await state.update_data(group=None)
            await callback_query.bot.send_message(
                callback_query.from_user.id,
                await get_choose_text("факультет"),
                reply_markup=await get_choose_keyboard(
                    "факультет", list((await get_dict_faculty()).keys())
                ),
            ),
        elif callback_query.data.split(" ")[1] == "дата":
            data = await state.get_data()
            if data.get("faculty", None) is None:
                await callback_query.answer(
                    "Должен быть выбран факультет", show_alert=True
                )
                await callback_query.message.delete()
                return

            faculties = await get_dict_faculty()
            groups = faculties[data["faculty"]]

            await callback_query.message.edit_text(
                text=await get_choose_text("группу"),
                reply_markup=await get_choose_keyboard("группа", groups),
            )
        elif callback_query.data.split(" ")[1] == "меню":
            await callback_query.message.edit_text(
                text=await get_choose_text("дату"),
                reply_markup=await get_schedule_menu_keyboard(),
            )


@router.callback_query(F.data.startswith("факультет"), MainState.main)
async def callback_choose_faculty(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    """Обработчик выбора факультета"""

    async with FSM(state_context=state, state=WaitState.wait) as state:
        _, index = callback_query.data.split(" ")
        faculties = await get_dict_faculty()
        await state.update_data(faculty=list(faculties.keys())[int(index)])
        await callback_query.message.edit_text(
            text=await get_choose_text("группу"),
            reply_markup=await get_choose_keyboard(
                "группа", faculties[list(faculties.keys())[int(index)]]
            ),
        )
        await callback_query.answer()


@router.callback_query(F.data.startswith("группа"), MainState.main)
async def callback_choose_group(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    """Обработчик выбора группы"""

    async with FSM(state_context=state, state=WaitState.wait) as state:
        _, index = callback_query.data.split(" ")
        data = await state.get_data()
        if data.get("faculty", None) is None:
            await callback_query.answer("Должен быть выбран факультет", show_alert=True)
            await callback_query.message.delete()
            return

        faculties = await get_dict_faculty()
        groups = faculties[data["faculty"]]
        await state.update_data(group=groups[int(index)])

        await callback_query.message.edit_text(
            text=await get_choose_text("дату"),
            reply_markup=await get_schedule_menu_keyboard(),
        )

        await callback_query.answer()


@router.callback_query(F.data.startswith("расписание"), MainState.main)
async def callback_choose_data(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    """Обработчик выбора даты"""

    async with FSM(state_context=state, state=WaitState.wait) as state:
        data = await state.get_data()

        if data.get("faculty", None) is None:
            await callback_query.answer("Должен быть выбран факультет", show_alert=True)
            await callback_query.message.delete()
            return

        if data.get("group", None) is None:
            await callback_query.answer("Должена быть задана группа", show_alert=True)
            await callback_query.message.delete()
            return

        await callback_query.message.edit_text(
            text=await get_schedule(data["group"], callback_query.data.split(" ")[2]),
            reply_markup=await get_back_keyboard(),
        )
