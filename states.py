from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    getting_tag = State()
    getting_album = State()
    getting_track = State()
