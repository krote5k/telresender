# -*- coding: utf-8 -*-
import config
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)

'''
def sender_verify(message_chat_id):
    if message_chat_id == int(config.sender_id):
        sender_name = config.sender_name
        print("Проверка 1")
        pass
    elif message_chat_id == int(config.sender_id_owner):
        sender_name = config.sender_name_owner
        print("Проверка 2")
        pass
    else:
        bot.send_message(message_chat_id, f"*{message.chat.username}* я тебя не знаю ", parse_mode = 'Markdown')
        print("Проверку не прошёл")
'''

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую. \n\n Отправьте /help для подсказки.')

@bot.message_handler(commands=["help"])
def helps(message):
    bot.send_message(message.chat.id, 'Просто отправляете сообщение и оно отправится участникам школьного чата')

@bot.message_handler(commands=["расписание"])
@bot.message_handler(regexp="^расписание$")
def send_rasp(message):
    bot.send_photo(config.chat, open('raspisanie.jpg', 'rb'))

"""
@bot.message_handler(commands=['w', 'п'])
@bot.message_handler(regexp="^.п$")
def send_weather(message):
    # get temperature ORSK
    r = requests.get(own_link)
    if r.status_code == 200:
        doc = xmltodict.parse(r.text)
        value = doc['current']['temperature']['@value']
        print('ORSK T:' + value)
        bot.send_message(message.chat.id, 'ORSK T: ' + value)
    else:
        bot.send_message(message.chat.id, u"cannot get content of ( URL: {own_link})... ERROR:" + str(r.status))
"""

@bot.message_handler(func=lambda message: message.reply_to_message is not None)
def reply(message):
    if message.reply_to_message.from_user.username == "atsip_d_bot":
        bot.forward_message(config.sender_id, config.chat, message.message_id)
    else:
        pass

@bot.message_handler(content_types=["text"])
def send_messages(message):
    if int(message.chat.id) == int(config.chat):
        try:
            chatId=message.text.split(': ')[0]
            text=message.text.split(': ')[1]
            bot.send_message(chatId, text)
        except:
            pass
    else:
        # При отправке не тем человеком - подставляется его ник
        if message.chat.id == int(config.sender_id):
            sender_name = config.sender_name
        else:
            sender_name = str(message.chat.username)

        bot.send_message(config.chat, f"*{sender_name}*: {message.text}", parse_mode = 'Markdown')
        bot.send_message(message.chat.id, f"*{message.from_user.first_name} {message.from_user.last_name}*  идет отправка 👍", parse_mode = 'Markdown')

@bot.message_handler(content_types=["photo"])
def send_photo(message):

    if int(message.chat.id) == int(config.chat):
        try:
            chatId=message.text.split(': ')[0]
            text=message.text.split(': ')[1]
            bot.send_message(chatId, text)
        except:
            pass
    else:
        # При отправке не тем человеком - подставляется его ник
        if message.chat.id == int(config.sender_id):
            sender_name = config.sender_name
        else:
            sender_name = str(message.chat.username)

        photo = message.photo[-1].file_id
        bot.send_photo(config.chat, photo, f"*{sender_name}*: {message.caption}", parse_mode='Markdown')
        bot.send_message(message.chat.id, f"*{message.chat.username}*, фото отправлено.", parse_mode = 'Markdown')


@bot.message_handler(content_types=["document"])
def send_doc(message):

    if int(message.chat.id) == int(config.chat):
        try:
            chatId=message.text.split(': ')[0]
            text=message.text.split(': ')[1]
            bot.send_message(chatId, text)
        except:
            pass
    else:
        # При отправке не тем человеком - подставляется его ник
        if message.chat.id == int(config.sender_id):
            sender_name = config.sender_name
        else:
            sender_name = str(message.chat.username)
 
        bot.forward_message(config.chat, message.chat.id, message.message_id) 
        bot.send_message(message.chat.id, "Переслал документ.")

if __name__ == '__main__':
    bot.polling(none_stop = True)
