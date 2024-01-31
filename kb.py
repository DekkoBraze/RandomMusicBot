from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="Get a random album by a tag", callback_data="get_album")],
    [InlineKeyboardButton(text="Get a random track by a genre", callback_data="get_track")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
