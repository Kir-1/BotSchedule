from aiogram.fsm.state import State, StatesGroup


class WaitState(StatesGroup):
    wait = State()
