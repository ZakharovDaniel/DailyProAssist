from aiogram.fsm.state import StatesGroup, State

class TaskState(StatesGroup):
    taskdescription = State()
    datetask = State()

class UpdateTaskState(StatesGroup):
    updatetask = State()