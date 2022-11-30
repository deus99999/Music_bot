from pytube import YouTube
import telebot
from telebot import types # для указание типов
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config import token

bot = telebot.TeleBot(token=token)


# markup = ReplyKeyboardMarkup(resize_keyboard=True)
#
# btn1 = types.KeyboardButton("Показать")
# btn2 = types.KeyboardButton("Посчитать")
# btn3 = types.KeyboardButton("Ввести стоимость за литр")
# markup.add(btn1, btn2)
# markup.add(btn3)
#
keyboard = InlineKeyboardMarkup()
keyboard.add(InlineKeyboardButton(text="Умножить на грн", callback_data="value"))

#youtube_video_url = 'https://www.youtube.com/watch?v=DkU9WFj8sYo'

#yt_obj = YouTube(youtube_video_url)


@bot.message_handler(content_types=['text'])
def buttons_menu(message):
    print(message)
    print(message.text)
    if message.text[:7] == "https:/":
        try:
            yt_obj = YouTube(message.text)
            song_title = yt_obj.title
            file_name = f"{song_title}" + ".mp3"

            yt_obj.streams.get_audio_only().download(filename=file_name)
            print('YouTube video audio downloaded successfully')
            audio = open(file_name, 'rb')
            print("audio was open")
            bot.send_audio(message.chat.id, audio)
            print("audio was send")

        except Exception as e:
            print(e)

    else:
        print("unvalid link")
        bot.send_message(message.chat.id, "Эта ссылка не работает")


bot.polling()
