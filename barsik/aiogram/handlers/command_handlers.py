from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command


class CommandHandlers:

    @classmethod
    async def current_state_handler(
            cls, message: types.Message,
            state: FSMContext,
    ):
        cur_state = await state.get_state()
        await message.answer(f"current state: {str(cur_state)}")

    @classmethod
    def register(cls, router: Router, **kwargs):
        router.message.register(cls.current_state_handler, Command("state"))
