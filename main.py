import telebot
from utils.parsing_structures import params_dict, directions_dict, params_list, names_dict
from config import TOKEN
from utils.table_loader import response

bot = telebot.TeleBot(TOKEN)

global_direction_param = ''
global_direction = ''
global_plan_param = ''
global_plan = ''


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    text = 'Добро пожаловать! С вами Бот-ассистент Магистрант.\nЯ показываю информацию по дисциплинам ИВМИИТ.\n' \
           'Выберите направление'
    keyboard = telebot.types.InlineKeyboardMarkup()
    for dir in params_dict.keys():
        sdir = str(dir)
        button = telebot.types.InlineKeyboardButton(text=sdir, callback_data=str(directions_dict[sdir]))
        keyboard.add(button)
    bot.send_message(chat_id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in [str(val) for val in directions_dict.values()])
def choose_plan(call):
    global global_direction_param
    global_direction_param = call.data
    message = call.message
    chat_id = message.chat.id

    dict = None
    for key in directions_dict.keys():
        if str(directions_dict[key]) == call.data:
            dict = params_dict[key]
            global global_direction
            global_direction = str(key)

    text = global_direction + '\nТеперь выберите учебный план'

    keyboard = telebot.types.InlineKeyboardMarkup()
    for dir in dict.keys():
        sdir = str(dir)
        button = telebot.types.InlineKeyboardButton(text=sdir, callback_data=str(dict[sdir]))
        keyboard.add(button)

    bot.send_message(chat_id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in params_list)
def choose_course(call):
    global global_plan_param
    global_plan_param = call.data
    message = call.message
    chat_id = message.chat.id

    for key in params_dict[global_direction]:
        if call.data == params_dict[global_direction][key]:
            global global_plan
            global_plan = str(key)

    text = global_direction + '\n' + global_plan + '\nТеперь выберите курс'
    keyboard = telebot.types.InlineKeyboardMarkup()
    if names_dict[global_direction] == 1:
        button1 = telebot.types.InlineKeyboardButton(text='1', callback_data='1')
        button2 = telebot.types.InlineKeyboardButton(text='2', callback_data='2')
        button3 = telebot.types.InlineKeyboardButton(text='3', callback_data='3')
        button4 = telebot.types.InlineKeyboardButton(text='4', callback_data='4')
        keyboard.add(button1, button2, button3, button4)
    if names_dict[global_direction] == 0:
        button1 = telebot.types.InlineKeyboardButton(text='1', callback_data='1')
        button2 = telebot.types.InlineKeyboardButton(text='2', callback_data='2')
        keyboard.add(button1, button2)

    bot.send_message(chat_id, text, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['1', '2', '3', '4'])
def send_data_message(call):
    course = call.data
    message = call.message
    chat_id = message.chat.id
    text = response(global_direction_param, global_plan_param, course)
    bot.send_message(chat_id, str(text))


@bot.message_handler(commands=['close'])
def close(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Сессия завершена!')
    bot.stop_bot()


@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    text = 'Я не знаю, что на это ответить!'
    bot.reply_to(message, text)


if __name__ == '__main__':
    bot.infinity_polling()
