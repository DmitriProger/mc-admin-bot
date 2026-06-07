from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

register_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📝 Подать заявку", callback_data="submit_application")],
    ]
)


rules_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="✅ Я прочитал правила", callback_data="rules_read")]
    ]
)


def admin_app(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Принять", callback_data=f"accept:{user_id}")],
            [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{user_id}")],
        ]
    )


user_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⚖️ Подать репорт", callback_data="report")],
        [InlineKeyboardButton(text="🤔 Задать вопрос", callback_data="question")],
    ]
)


cancel_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]]
)


report_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Гриферство", callback_data="Griefing"),
            InlineKeyboardButton(text="Территории", callback_data="Territories"),
        ],
        [
            InlineKeyboardButton(text="Тех. часть", callback_data="technical"),
            InlineKeyboardButton(text="Общение", callback_data="communication"),
        ],
        [InlineKeyboardButton(text="Другое (напишу сам)", callback_data="other")],
    ]
)


back_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]]
)


def admin_report(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ответить", callback_data=f"answer:{user_id}")],
            [InlineKeyboardButton(text="Закрыть", callback_data=f"close:{user_id}")],
        ]
    )
