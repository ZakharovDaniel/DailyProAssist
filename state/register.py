from aiogram.fsm.state import StatesGroup, State

class RegisterState(StatesGroup):
    registerName = State()
    registerPhone = State()
