from aiogram.filters.state import StatesGroup, State

class CoursesState(StatesGroup):
    course = State()
    lesson = State()
    paragraph = State()
    text = State()