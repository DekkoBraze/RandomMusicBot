from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    getting_album_tag = State()
