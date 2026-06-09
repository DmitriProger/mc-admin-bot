from aiogram.fsm.state import State, StatesGroup


class ApplicationForm(StatesGroup):
    nickname = State()
    age = State()
    experience = State()
    plans = State()
    rp_situation = State()
    rules = State()


class ReportForm(StatesGroup):
    nick_offender = State()
    violation_type = State()
    custom_violation = State()
    description = State()


class AdminStates(StatesGroup):
    admin_answer = State()
