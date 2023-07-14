from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard_buttons = [
    KeyboardButton('Увидеть меня📸'),
    KeyboardButton('Узнать мои увлечения⚽️'),
    KeyboardButton('Послушать меня🎧'),
]

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

for button in main_keyboard_buttons:
    main_keyboard.add(button)


photo_keyboard_buttons = [
    KeyboardButton('Свежее(не совсем) селфи🤳'),
    KeyboardButton('Фото из старшей школы🏫'),
    KeyboardButton('Вернуться в главное меню⬅')
]

photo_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for button in photo_keyboard_buttons:
    photo_keyboard.add(button)


story_keyboard_buttons = [
    KeyboardButton('Мой рассказ о GPT🧠'),
    KeyboardButton('Я объясняю разницу между SQL и NoSQL📚'),
    KeyboardButton('История первой любви❤️'),
    KeyboardButton('Вернуться в главное меню⬅')
]

story_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for button in story_keyboard_buttons:
    story_keyboard.add(button)


nextstep_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Вернуться в главное меню⬅'))
