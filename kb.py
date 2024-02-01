from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

get_tag = [
    [InlineKeyboardButton(text="Find music by a tag", callback_data="get_tag")]
]
get_tag = InlineKeyboardMarkup(inline_keyboard=get_tag)

album_or_track = [
    [InlineKeyboardButton(text="Get an album", callback_data="get_album")],
    [InlineKeyboardButton(text="Get a track", callback_data="get_track")]
]
album_or_track = InlineKeyboardMarkup(inline_keyboard=album_or_track)


def url_buttons(last_fm_url):
    url_menu = [
        [InlineKeyboardButton(text="last.fm", url=last_fm_url)]
    ]
    url_menu = InlineKeyboardMarkup(inline_keyboard=url_menu)

    return url_menu
