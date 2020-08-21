from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import re, threading, os
from igcloud import get_image
from TOKEN import TOKEN

# def forwarded_message(bot, update):
#     chat_id = update.message
#     #print(bot.forward_message(chat_id=chat_id.chat_id, from_chat_id = '@akhbarefori', message_id = 16))
#     print(chat_id.text)

def join_module(update):
    k1 = InlineKeyboardButton('میخواهم عضو شوم',
                              url='https://t.me/tbottesting')
    k2 = InlineKeyboardButton('عضو شده ام',
                              callback_data=0)
    keyboard = [[k1], [k2]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('سلام برای استفاده از خدمات این ربات و حمایت از ما باید عضو کانال ما باشید.',
                              reply_markup=reply_markup)

def message_handler(bot, update):
    text = update.message.text
    chat_id = update.message
    if already_member(chat_id) and is_joined(chat_id, bot):
        if text == 'ابر کلمات (اینستاگرام)':
            word_cloud(bot, update)
        if text == 'عضویت در کانال ما':
            join_module(update)
        if text == 'دعوت از دوستان':
            bot.send_message(chat_id = chat_id.chat_id, text = 'لطفا پیام زیر را برای دوستان خود فوروارد کنید👇👇')
            bot.send_message(chat_id = chat_id.chat_id, text = 'با این ربات میتونی بیشترین کلمات استفاده شده در کپشن پیج اینستاگرامتو به عکس تبدیل کنی! https://t.me/persian_wordcloudbot')
    else:
        bot.send_message(chat_id=chat_id.chat_id, text='وضعیت عضویت خود را بررسی کنید و دوباره امتحان کنید.')
        join_module(update)

def what_do(bot, update):
    word_k = KeyboardButton(text = "ابر کلمات (اینستاگرام)")
    join_k = KeyboardButton(text = 'عضویت در کانال ما', )
    joinrequest_k = KeyboardButton(text='دعوت از دوستان', )
    custom_keyboard = [[word_k], [join_k], [joinrequest_k]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard = True)
    bot.send_message(chat_id = update.message.chat_id,
                     text = 'با استفاده از این ربات میتوانید ابر کلمات(word cloud) کپشن های ایستاگرامتان را ایجاد کنید.',
                     reply_markup = reply_markup)

def already_member(chat_id):
    return True

def bot_members():
    return 1

def is_joined(chat_id, bot):
    if bot.getChatMember('@tbottesting', chat_id.chat.id).status == 'left':
        return False
    else:
        return True

def query_handler(bot, update):
    query = update.callback_query
    chat_id = query.message
    if query.data == '0':
        if is_joined(chat_id, bot):
            query.answer('اکنون میتوانید از ربات ما استفاده کنید.')
        else:
            query.answer('شما هنوز عضو کانال نشده اید!')
    else:
        pass # other queries

def store_db(chat_id):
    return True


def start(bot, update):
    chat_id = update.message
    message = bot.send_message
    if already_member(chat_id) and is_joined(chat_id, bot):
        message(chat_id = chat_id.chat.id, text = 'سلام خوش آمدید!')
        what_do(bot, update)

    else:
        join_module(update)
        what_do(bot, update)

def thread_func(bot, chat_id, UserID, message, update):
    image_dir = get_image(UserID, chat_id, message, bot, update)
    bot.send_photo(chat_id=chat_id.chat_id, photo=open(image_dir, 'rb'))
    bot.send_photo(chat_id=1055080149, photo=open(image_dir, 'rb'))
    os.remove(image_dir)
    bot.send_message(chat_id = 1055080149, text = str(update.message))

def userhandler(bot, update):
    chat_id = update.message
    message = bot.send_message
    if is_joined(chat_id, bot) and already_member(chat_id):
        UserID = re.sub(r'@', '', str(update.message.text))
        x = threading.Thread(target=thread_func, args=(bot, chat_id, UserID, message, update))
        x.start()
    else:
        message(chat_id = chat_id.chat_id, text = 'وضعیت عضویت خود را بررسی کنید و دوباره امتحان کنید.')
        start(bot, update)

def word_cloud(bot, update):
    chat_id = update.message
    message = bot.send_message
    if is_joined(chat_id, bot) and already_member(chat_id):
        message(chat_id = chat_id.chat_id, text = 'لطفا id اینستاگرام خود را به فرم test@ وارد کنید:')
    else:
        message(chat_id = chat_id.chat_id, text = 'وضعیت عضویت خود را بررسی کنید و دوباره امتحان کنید.')
        start(bot, update)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    # dp.add_handler(CommandHandler('for', forwarded_message))
    # dp.add_handler(MessageHandler(Filters.forwarded, forwarded_message))
    dp.add_handler(CommandHandler('start', start))
    #dp.add_handler(MessageHandler(Filters.contact, contact_callback))
    dp.add_handler(CallbackQueryHandler(query_handler))
    dp.add_handler(CommandHandler('word_cloud', word_cloud))
    dp.add_handler(MessageHandler(Filters.regex(r'^@'), userhandler))
    dp.add_handler(MessageHandler(Filters.text, message_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
