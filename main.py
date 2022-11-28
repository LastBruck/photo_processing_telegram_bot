import telebot, os, time
from telebot import types
from pathlib import Path
from src import methods
from dotenv import load_dotenv
load_dotenv()



bot = telebot.TeleBot(os.getenv("SECRET_KEY"))

images = {}

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>\nЯ бот по удалению заднего фона или распознаванию текста с твоей фотографии.\nНажми <b>кнопку</b> что выполнить.'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Удалить задний фон')
    button2 = types.KeyboardButton('Распознать текст')
    button3 = types.KeyboardButton('help')
    markup.add(button1, button2)
    markup.add(button3)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Удалить задний фон':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Меню')
            markup.add(button1)
            bot.send_message(message.chat.id, "Пришли фото в формате <b>.jpg</b> или <b>.png</b>, откуда удалить задний фон.", parse_mode='html', reply_markup=markup)
            bot.register_next_step_handler(message, remove)
        elif message.text == 'Распознать текст':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Меню')
            markup.add(button1)
            bot.send_message(message.chat.id, "Пришли фото в формате <b>.jpg</b> или <b>.png</b> с текстом, что бы его распознать.", parse_mode='html', reply_markup=markup)
            bot.register_next_step_handler(message, text_img)
        elif message.text == 'help' or 'Меню':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Удалить задний фон')
            button2 = types.KeyboardButton('Распознать текст')
            button3 = types.KeyboardButton('help')
            markup.add(button1, button2)
            markup.add(button3)
            bot.send_message(message.from_user.id, 'Нажми что нужно сделать', parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['photo', 'document'])
def save_photo(message):
    images[str(message.chat.id)] = []
    Path(f'input/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    Path(f'output/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    try:
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'input/{message.chat.id}/' + file_info.file_path.replace('photos/', '')
            images[str(message.chat.id)].append(src)
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
                
        elif message.content_type == 'document':
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'input/{message.chat.id}/' + file_info.file_path.replace('documents/', '')
            images[str(message.chat.id)].append(src)
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
    except Exception as e:
        bot.reply_to(message,e )


@bot.message_handler(content_types=['photo', 'document'])
def remove(message):
    try:
        save_photo(message)
        for img in images[str(message.chat.id)]:
            reply_img = methods.remove_bg(message.chat.id, img)
            time.sleep(1)
            bot.send_document(message.chat.id, open(reply_img, 'rb'), caption='DONE!')
    except:
        bot_message(message)


@bot.message_handler(content_types=['photo', 'document'])
def text_img(message):
    try:
        save_photo(message)
        for img in images[str(message.chat.id)]:
            text = methods.text_from_img(message.chat.id, img)
            time.sleep(1)
            bot.send_message(message.from_user.id, text)
    except:
        bot_message(message)


bot.polling(none_stop=True)
