from aiogram import Bot, Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage


"""
Bot object and dispatcher initialization 
"""
bot = Bot(token=os.getenv('TOKEN'))

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

API_key = os.getenv('API')

MY_TG_ID = os.getenv('MY_TG_ID')
