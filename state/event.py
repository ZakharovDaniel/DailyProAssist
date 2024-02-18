from aiogram.filters.state import StatesGroup, State

class EventState(StatesGroup):
    place = State()
    date = State()
    time = State()
    desciption = State()


