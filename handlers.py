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

router = Router()
network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=pylast.md5(password),
)


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.callback_query(F.data == "get_album")
async def get_album_tag(clbck: CallbackQuery, state: FSMContext):
    await clbck.bot.send_message(clbck.message.chat.id, text.get_tag)
    await state.set_state(BotStates.getting_album_tag)


@router.message(BotStates.getting_album_tag)
async def get_random_album(msg: Message, state: FSMContext):
    tag = network.get_tag(msg.text)
    albums = tag.get_top_albums(500)
    album_num = random.randint(0, 499)
    album = albums[album_num]
    print(album.item.artist, ' - ', album.item.title)

#@router.message(BotStates.getting_genre)
#async def search_album(msg: Message, state: FSMContext):
#    query = 'genre:' + msg.text.replace(' ', '%')
#    random_offset = random.randint(0, 100)
#    print(random_offset)
#    async with spotify.Client(CLIENT_ID, CLIENT_SECRET) as client:
#        results = await client.search(query, types=['track'], limit=50, offset=random_offset)
#        for track in results.tracks:
#            if track.popularity > 40:
#                print(track.artist.name + ' - ' + track.name)
#    await state.clear()
