import os
from pytube import YouTube
from aiogram import *
from config import token
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token)
dp = Dispatcher(bot)

arguments = []


@dp.message_handler()
async def text_message(message:types.Message):
    chat_id = message.chat.id
    url = message.text
    yt = YouTube(url)

    arguments.append(url)
    arguments.append(chat_id)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="720p", callback_data=f"video|{0}|{1}"))
    keyboard.add(InlineKeyboardButton(text="Music", callback_data=f"music|{0}|{1}"))

    if message.text.startswith("https://www.youtube.com"):
        await bot.send_message(chat_id, f"{yt.title}",
                               reply_markup=keyboard,
                               parse_mode="Markdown")




@dp.message_handler(commands=["start"])
async def start_message(message:types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Привет, чтобы скачать видео отправь мне ссылку на видео с YouTube!")


async def download_youtube_video(url, chat_id, bot):
    try:
        yt = YouTube(url)
        await bot.send_message(chat_id, "Файл загружается..")

        stream = yt.streams.filter(progressive=True, file_extension="mp4")
        stream.get_highest_resolution().download(f"{chat_id}", f"{chat_id}_{yt.title}")

        with open(f"{chat_id}/{chat_id}_{yt.title}", "rb") as video:
            await bot.send_video(chat_id, video, parse_mode="Markdown")
            os.remove(f"{chat_id}/{chat_id}_{yt.title}")
    except:
        await bot.send_message(chat_id, "Не удалось загрузить видеофайл")


async def download_youtube_music(url, chat_id, bot):
    try:
        yt = YouTube(url)
        await bot.send_message(chat_id, "Файл загружается..")

        audio = yt.streams.get_audio_only()
        audio.download(f"{chat_id}", f"{yt.title}.mp3")
        print("file was open")


        with open(f"{chat_id}/{yt.title}.mp3", "rb") as music:
            await bot.send_audio(chat_id, music, parse_mode="Markdown")
            #os.remove(f"{chat_id}/{chat_id}_{yt.title}")
    except:
        await bot.send_message(chat_id, "Не удалось загрузить аудиофайл")


# @dp.callback_query_handler(lambda c: c.data == 'video')
# async def send_video(callback_query: types.CallbackQuery):
#     await callback_query.message.answer('Видео вроде как должно было начать загружаться, но..')


@dp.callback_query_handler(lambda c: c.data.startswith('video'))
async def send_video(callback_query: types.CallbackQuery):
    _, url_index, chat_id_index = callback_query.data.split("|")
    await download_youtube_video(arguments[int(url_index)], arguments[int(chat_id_index)], bot)


@dp.callback_query_handler(lambda c: c.data.startswith('music'))
async def send_audio(callback_query: types.CallbackQuery):
    _, url_index, chat_id_index = callback_query.data.split("|")
    await download_youtube_music(arguments[int(url_index)], arguments[int(chat_id_index)], bot)


if __name__ == "__main__":
    executor.start_polling(dp)
