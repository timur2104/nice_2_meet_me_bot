from aiogram.dispatcher.filters.state import State, StatesGroup


class AllStates(StatesGroup):
    main_menu = State()
    photo_menu = State()
    voice_menu = State()
    wait_message = State()
