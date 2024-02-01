from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

get_tag = [
    [InlineKeyboardButton(text="Find music by a tag", callback_data="get_tag")]
]
get_tag = InlineKeyboardMarkup(inline_keyboard=get_tag)

album_or_track = [
    [InlineKeyboardButton(text="Get a track", callback_data="get_track")],
    [InlineKeyboardButton(text="Get an album", callback_data="get_album")]

]
album_or_track = InlineKeyboardMarkup(inline_keyboard=album_or_track)


def ger_url_menu(last_fm_url, youtube_url=''):
    if youtube_url:
        url_menu = [
            [InlineKeyboardButton(text="last.fm", url=last_fm_url)],
            [InlineKeyboardButton(text="YouTube", url=youtube_url)]
        ]
    else:
        url_menu = [
            [InlineKeyboardButton(text="last.fm", url=last_fm_url)]
        ]
    url_menu = InlineKeyboardMarkup(inline_keyboard=url_menu)

    return url_menu


def get_tags_menu(tags):
    builder = ReplyKeyboardBuilder()
    for tag in tags:
        builder.add(KeyboardButton(text=tag))
    builder.adjust(5)
    tags_menu = builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

    return tags_menu


def get_restart_menu(data):
    restart_menu = [
        [InlineKeyboardButton(text="Repeat", callback_data=data)],
        [InlineKeyboardButton(text="Write a new tag", callback_data="get_tag")]
    ]
    restart_menu = InlineKeyboardMarkup(inline_keyboard=restart_menu)

    return restart_menu
