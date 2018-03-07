import telebot
from telebot import types
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU')
from telegramcalendar import create_calendar
from telebot import types

bot = telebot.TeleBot('')
current_shown_dates={}

@bot.message_handler(commands=['calendar'])
def get_calendar(message):
    now = datetime.datetime.now() #Current date
    chat_id = message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = date #Saving the current date in a dict
    markup= create_calendar(now.year,now.month)
    bot.send_message(message.chat.id, "Please, choose a date", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        day=call.data[13:]
        date = datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(day))

        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(course) for course in ["1 курс", "2 курс"]])
        msg = bot.send_message(chat_id, "Расписание на " + str(date.strftime('%d.%m.%y')) + "\n(выбери курс)",
            reply_markup=keyboard)
        bot.register_next_step_handler(msg,name)
        bot.answer_callback_query(call.id, text="hkhkjhkjhj")

    else:
        #Do something to inform of the error
        pass

def name(m):
    if m.text== "1 курс":
        bot.send_message(m.chat.id, 'здесь расписание для *первого* курса',
                         parse_mode='Markdown')
    elif m.text== "2 курс":
        bot.send_message(m.chat.id, 'здесь расписание для *второго* курса',
                         parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if(saved_date is not None):
        year,month = saved_date
        month-=1
        if month<1:
            month=12
            year-=1
        date = (year,month)
        current_shown_dates[chat_id] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        #Do something to inform of the error
        pass

@bot.callback_query_handler(func=lambda call: call.data == 'ignore')
def ignore(call):
    bot.answer_callback_query(call.id, text="")


bot.polling()