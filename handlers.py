from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from config import API_KEY, API_SECRET, username, password
from aiogram.fsm.context import FSMContext
from states import BotStates
import random
import pylast

import kb
import text

tag_text = ''
router = Router()
network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=pylast.md5(password),
)


@router.message(Command("start"))
async def start_handler(msg: Message):
    global tag_text
    tag_text = ''
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.get_tag)


@router.callback_query(F.data == "get_tag")
async def get_album_tag(clbck: CallbackQuery, state: FSMContext):
    tags = network.get_top_tags(50)
    tags = [tag.item.name for tag in tags]
    buttons = kb.get_tags_menu(tags)
    await clbck.bot.send_message(clbck.message.chat.id, text.get_tag, reply_markup=buttons)
    await state.set_state(BotStates.getting_tag)


@router.message(BotStates.getting_tag)
async def get_album_tag(msg: Message, state: FSMContext):
    global tag_text
    tag_text = msg.text
    await msg.answer('Do you need album or track?', reply_markup=kb.album_or_track)


@router.callback_query(F.data == "get_album")
@router.callback_query(F.data == "get_track")
async def get_random_album(clbck: CallbackQuery, state: FSMContext):
    global tag_text
    tag = network.get_tag(tag_text.lower())
    if clbck.data == 'get_album':
        entities = tag.get_top_albums(250)
    else:
        entities = tag.get_top_tracks(250)
    entity_num = random.randint(0, len(entities) - 1)
    try:
        entity = entities[entity_num]
        entity_cover = entity.item.get_cover_image()
        entity_url = entity.item.get_url()
        entity_playcount = str(entity.item.get_playcount())
        keyboard = kb.ger_url_menu(entity_url)
        answer = (entity.item.artist.name + ' - ' + entity.item.title + '\n\n' + 'Playcount: ' +
                  entity_playcount)
        await clbck.bot.send_photo(clbck.message.chat.id, entity_cover, caption=answer, reply_markup=keyboard)
        await state.clear()
        restart_menu = kb.get_restart_menu(clbck.data)
        await clbck.bot.send_message(clbck.message.chat.id, "What's next?", reply_markup=restart_menu)
    except IndexError:
        await clbck.bot.send_message(clbck.message.chat.id, 'Irrelevant tag. Please, try again.')
