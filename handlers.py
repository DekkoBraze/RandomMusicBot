import pylast
from pyyoutube import Api

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext


import random

import kb
import text
from states import BotStates
from config import API_KEY, API_SECRET, USERNAME, PASSWORD, API_YOUTUBE

router = Router()
network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=USERNAME,
    password_hash=pylast.md5(PASSWORD),
)
youtube_api = Api(api_key=API_YOUTUBE)


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.get_tag)


@router.callback_query(F.data == "get_tag")
async def get_album_tag(clbck: CallbackQuery, state: FSMContext):
    await state.clear()
    tags = network.get_top_tags(50)
    tags = [tag.item.name for tag in tags]
    buttons = kb.get_tags_menu(tags)
    await clbck.bot.send_message(clbck.message.chat.id, text.get_tag, reply_markup=buttons)
    await state.set_state(BotStates.getting_tag)


@router.message(BotStates.getting_tag)
async def get_album_tag(msg: Message, state: FSMContext):
    await msg.answer('Do you need album or track?', reply_markup=kb.album_or_track)
    await state.update_data(tag_text=msg.text)


@router.callback_query(F.data == "get_album")
@router.callback_query(F.data == "get_track")
async def get_random_album(clbck: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    tag = network.get_tag(data['tag_text'].lower())
    if clbck.data == 'get_album':
        entities = tag.get_top_albums(250)
    else:
        entities = tag.get_top_tracks(250)
    entity_num = random.randint(0, len(entities) - 1)
    try:
        entity = entities[entity_num]
        entity_cover = entity.item.get_cover_image()
        entity_artist_title = entity.item.artist.name + ' - ' + entity.item.title
        entity_url = entity.item.get_url()
        entity_playcount = str(entity.item.get_playcount())
        try:
            r = youtube_api.search_by_keywords(q=entity_artist_title, search_type=["video"], count=1, limit=1)
            entity_youtube = 'https://www.youtube.com/watch?v=' + r.items[0].id.videoId
            keyboard = kb.ger_url_menu(entity_url, entity_youtube)
        except Exception as e:
            print(e)
            await clbck.bot.send_message(clbck.message.chat.id, "Can't get a youtube video.")
            keyboard = kb.ger_url_menu(entity_url)
        answer = (entity_artist_title + '\n\n' + 'Playcount: ' + entity_playcount)
        await clbck.bot.send_photo(clbck.message.chat.id, entity_cover, caption=answer, reply_markup=keyboard)
        restart_menu = kb.get_restart_menu(clbck.data)
        await clbck.bot.send_message(clbck.message.chat.id, "What's next?", reply_markup=restart_menu)
    except IndexError:
        await clbck.bot.send_message(clbck.message.chat.id, 'Irrelevant tag. Please, try again.')
