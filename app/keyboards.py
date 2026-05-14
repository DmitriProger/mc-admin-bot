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


def admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Принять", callback_data=f"accept:{user_id}")],
            [InlineKeyboardButton(text="❌ Отклонить", callback_data=f"reject:{user_id}")],
        ]
    )
