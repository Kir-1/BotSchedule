from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from src.fsm.main_state import MainState


class FSM:

    def __init__(self, state_context: FSMContext, state: State):
        self.state_context = state_context
        self.state = state
        self.base_state = MainState.main

    async def __aenter__(self):
        await self.state_context.set_state(self.state)
        return self.state_context

    async def __aexit__(self, exception_type, exception_val, trace):
        if self.base_state:
            await self.state_context.set_state(self.base_state)
        else:
            await self.state_context.clear()
