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
