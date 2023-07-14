import io

from create_bot import dp, bot, API_key, MY_TG_ID
from keyboards import main_keyboard, photo_keyboard, story_keyboard, nextstep_keyboard
from states import AllStates
from speech_to_text_API import speech_to_text_pipeline
from answering_model import query

from aiogram import executor, types
from aiogram.dispatcher import FSMContext


async def start_handler(message: types.Message):
    """
    Handler for /start command, restarting the bot and returning it to default state
    """
    # Deleting command message
    await bot.delete_message(message_id=message.message_id,
                             chat_id=message.from_user.id)

    # Setting state to main_menu, to use this command as bot restart from any state
    await AllStates.main_menu.set()

    # Sending hello message with bot interface and functionality info
    await bot.send_message(text='Привет, это тестовый бот, который познакомит тебя с кандидатом в наставники kids ai.\n '
                                '\t1. Основной функционал бота доступен с помощью кнопок ниже '
                                ', с их помощью ты можешь увидеть, узнать о хобби или даже послушать рассказы на серьезные и не очень темы '
                                'от разработчика бота\n '
                                '\t2. Ты также можешь отправить мне голосовое сообщение, а я постараюсь ответить тебе, '
                                'но предупреждаю, что загруженный в меня контекст не позваляет отвечать на все вопросы, ',
                           chat_id=message.from_user.id,
                           reply_markup=main_keyboard,
                           parse_mode='HTML')


async def handle_source(message: types.Message):
    """
    Handler sending link to Github repository containing source code of the project.
    """
    await bot.delete_message(message_id=message.message_id,
                             chat_id=message.from_user.id)

    await bot.send_message(text='[Ссылка](https://github.com/) на репозиторий с исходным кодом',
                           chat_id=message.from_user.id,
                           parse_mode='Markdown')


async def handle_nextstep(message: types.Message):
    """
    Handler for command that will notify candidate about his next step
    """

    await bot.delete_message(message_id=message.message_id,
                             chat_id=message.from_user.id)

    await AllStates.wait_message.set()

    await bot.send_message(text='Отправь сообщение и кандидат в наставники его обязательно получит',
                           chat_id=message.from_user.id,
                           parse_mode='HTML',
                           reply_markup=nextstep_keyboard)


async def send_nextstep(message: types.Message):
    """
    Handler copying message sent to bot to direct it to developer
    """

    try:
        await bot.copy_message(chat_id=MY_TG_ID,
                               from_chat_id=message.from_user.id,
                               message_id=message.message_id)
    except:
        await bot.send_message(text='Не удалось отправить сообщение.',
                               chat_id=message.from_user.id,
                               parse_mode='HTML',
                               reply_markup=nextstep_keyboard)
    else:
        await bot.send_message(text='Сообщение отправлено.',
                               chat_id=message.from_user.id,
                               parse_mode='HTML',
                               reply_markup=nextstep_keyboard)
    await back_to_main(message)


async def photo_request_handler(message: types.Message):
    """
    Handler moving user to photo menu followed with info about this section functionality
    """
    await AllStates.photo_menu.set()

    # await bot.delete_message(message_id=message.message_id,
    #                          chat_id=message.from_user.id)

    await bot.send_message(text='Конечно, кандидата надо знать в лицо. \n'
                                'Он подготовил для тебя два фото, какое посмотреть - выбор за тобой',
                           chat_id=message.from_user.id,
                           reply_markup=photo_keyboard,
                           parse_mode='HTML')


async def send_photo(message: types.Message):
    """
     Handler sending photo requested by user in photo menu
    """
    if message.text == 'Свежее(не совсем) селфи🤳':
        photo_path = 'data/me_now.jpeg'
        caption = 'Это фото кандидата пару лет назад'
    else:
        photo_path = 'data/me_school.jpg'
        caption = 'А это кандидат в наставники в свои школьные годы'

    with open(photo_path, 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=photo,
                             caption=caption)


async def interest_request_handler(message: types.Message):
    """
    Handler sending user text message about my main hobby
    """

    with open('data/football.jpeg', 'rb') as photo:
        with io.open('data/my_hobby.txt', encoding='utf-8') as caption_file:
            await bot.send_photo(chat_id=message.from_user.id,
                                 photo=photo,
                                 caption=caption_file.read(),
                                 parse_mode='HTML')


async def story_request_handler(message: types.Message):
    """
    Handler moving user to voice stories menu followed with info about this section functionality
    """
    await AllStates.voice_menu.set()

    await bot.send_message(text='А здесь ты можешь послушать истории, записанные кандидатом в наставники,'
                                ' выбери интересующую тебя с помощью кнопок ниже.',
                           chat_id=message.from_user.id,
                           reply_markup=story_keyboard,
                           parse_mode='HTML')


async def send_voice_story(message: types.Message):
    """
    Handler sending the story requested by user in format of voice message
    """
    if message.text == 'Мой рассказ о GPT🧠':
        voice_file = open('data/GPT.m4a', 'rb')
    elif message.text == 'Я объясняю разницу между SQL и NoSQL📚':
        voice_file = open('data/SQL.m4a', 'rb')
    else:
        voice_file = open('data/Lovestory.m4a', 'rb')

    await bot.send_voice(chat_id=message.from_user.id,
                         voice=voice_file)

    voice_file.close()


async def voice_handler(message: types.Message, state: FSMContext):
    msg = await bot.send_message(text='Дай мне минутку послушать, что ты сказал..',
                                 chat_id=message.from_user.id,
                                 parse_mode='HTML')

    voice = io.BytesIO()
    await message.voice.download(destination_file=voice)

    transcription = await speech_to_text_pipeline(voice, API_key)

    model_payload = {
        "inputs": {
            "question": transcription['results']['transcript'],
            "context": "Привет! "
                       "У меня все супер! "
                       "Я тестовый чат бот для задания кандидата в наставники kids ai. "
                       "Меня разработал Сергеев Тимур. "
                       "Тимур студент второго курса магистратуры Университета Иннополис, увлекается ИИ и бэкенд-разработкой. "
                       "Я отвечаю на вопросы с помощью общедоступной модели AlexKay/xlm-roberta-large-qa-multilingual-finedtuned-ru."
        },
    }
    while True:
        response = await query(model_payload)
        print(response)
        if 'answer' in response.keys():
            break
    await msg.edit_text(text=response['answer'])


async def back_to_main(message: types.Message):
    await AllStates.main_menu.set()

    await bot.delete_message(message_id=message.message_id,
                             chat_id=message.from_user.id)

    await bot.send_message(text='Ты снова в главном меню.',
                           chat_id=message.from_user.id,
                           reply_markup=main_keyboard,
                           parse_mode='HTML')

dp.register_message_handler(start_handler, commands=['start'], state=['*'])
dp.register_message_handler(handle_source, commands=['source'], state=['*'])
dp.register_message_handler(handle_nextstep, commands=['nextstep'], state=['*'])

dp.register_message_handler(back_to_main, text=['Вернуться в главное меню⬅'], state=[AllStates.photo_menu, AllStates.voice_menu, AllStates.wait_message])

dp.register_message_handler(photo_request_handler, text=['Увидеть меня📸'], state=[AllStates.main_menu, None])
dp.register_message_handler(send_photo, text=['Свежее(не совсем) селфи🤳', 'Фото из старшей школы🏫'], state=[AllStates.photo_menu])

dp.register_message_handler(interest_request_handler, text=['Узнать мои увлечения⚽️'], state=[AllStates.main_menu, None])
dp.register_message_handler(send_voice_story, text=['Мой рассказ о GPT🧠', 'Я объясняю разницу между SQL и NoSQL📚', 'История первой любви❤️'], state=[AllStates.voice_menu])

dp.register_message_handler(story_request_handler, text=['Послушать меня🎧'], state=[AllStates.main_menu, None])

dp.register_message_handler(send_nextstep, content_types=types.ContentTypes.ANY, state=[AllStates.wait_message])

dp.register_message_handler(voice_handler, content_types=types.ContentTypes.VOICE, state=['*'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
