from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

register_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📝 Подать заявку", callback_data="submit_application")],
    ]
)
