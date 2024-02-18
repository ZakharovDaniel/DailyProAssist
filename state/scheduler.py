from aiogram.fsm.state import StatesGroup, State

class DateSchedulerState(StatesGroup):
    date = State()
