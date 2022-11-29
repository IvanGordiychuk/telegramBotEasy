import telebot
from telebot import types
from pymongo import MongoClient
#f
connect_to_mongo=""
name_of_db = "TelegramDB"
name_of_collection = "TelegramColl"
client = MongoClient(connect_to_mongo)

db = client["TelegramDB"]
collection = db["TelegramColl"]


bot = telebot.TeleBot()

name = ''
surname = ''
age = 0
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, 'What is your name?')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Write '/reg'")


def get_name(message):
   global name
   name = message.text
   bot.send_message(message.from_user.id, 'What is your surname?')
   bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'What is your age?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:
        try:
            age = int(message.text)
        except:
            bot.send_message(message.from_user.id, 'Numbers, pls!!!')
    keyword = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes')
    keyword.add(key_yes)
    key_no = types.InlineKeyboardButton(text='No', callback_data='no')
    keyword.add(key_no)
    question = "Your age is " + str(age) + " name is " + name + " surname is " + surname
    bot.send_message(message.from_user.id,text=question, reply_markup=keyword)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        print("код сохранения данных, или их обработки")
        bot.send_message(call.message.chat.id, 'Запомню : )')
        collection.insert_one({
            'age': age,
            "name": name,
            "surname": surname
        })

    elif call.data == "no":
         print("переспрашиваем")


bot.polling(none_stop=True, interval=0)