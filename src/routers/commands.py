from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.fsm.main_state import MainState
from src.texts.commands import get_command_start_text
from src.keyboards.reply import get_main_menu_keyboard


router = Router(name=__name__)


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """Обработчик команды старт"""

    await message.answer(
        await get_command_start_text(message.from_user.username),
        reply_markup=await get_main_menu_keyboard(),
    )

    await state.update_data(faculty=None, group=None)
    await state.set_state(MainState.main)
