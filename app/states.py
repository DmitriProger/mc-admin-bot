from aiogram.fsm.state import State, StatesGroup


class ApplicationForm(StatesGroup):
    nickname = State()
    age = State()
    experience = State()
    plans = State()
    rp_situation = State()
    rules = State()
