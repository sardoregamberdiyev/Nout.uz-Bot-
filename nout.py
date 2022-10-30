from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

from service import *

import ast

try:
    create_table()
    create_table_log()
except Exception as e:
    pass

bts = [
    [KeyboardButton("🌇 Tashkent"), KeyboardButton("🌇 Farg'ona")],
    [KeyboardButton(" Andijon🌇"), KeyboardButton(" Jizzax🌇")],
    [KeyboardButton("🌇 Sirdaryo"), KeyboardButton("🌇 Surxondaryo")],
    [KeyboardButton(" Samarqand🌇"), KeyboardButton(" Buxoro🌇")],
    [KeyboardButton("🌇 Namangan"), KeyboardButton("🌇 Navoiy")],
    [KeyboardButton(" Xorazm🌇"), KeyboardButton(" Qashqadaryo🌇")]
]


def btns(tip, msg=""):
    btn = []
    if tip == "ctg":
        ctgs = get_ctgs()
        for i in range(1, len(get_ctgs()), 2):
            btn.append([KeyboardButton(ctgs[i - 1][1]), KeyboardButton(ctgs[i][1])])

        if len(ctgs) % 2 == 1:
            btn.append([KeyboardButton(ctgs[-1][1])])

    elif tip == "ctgs":
        products = get_product(msg)
        for i in range(1, len(products), 2):
            btn.append([KeyboardButton(products[i - 1][1]), KeyboardButton(products[i][1])])

        if len(products) % 2 == 1:
            btn.append([KeyboardButton(products[-1][1])])

        btn.append([KeyboardButton("Back")])

    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


contact = [
    [KeyboardButton("contact", request_contact=True)]
]


def str_to_dict(strr):
    return ast.literal_eval(strr)


def to_dict(strr):
    return ast.literal_eval(strr)


def start(update, context):
    user = update.message.from_user
    try:
        create_user_log(user_id=user.id)
        create_user(user_id=user.id, username=user.username)
    except Exception as e:
        pass
    clear_state(user.id, clear=10)
    log = to_dict(get_user_log(user.id)[0])
    if log["state"] == 10:
        update.message.reply_text("Katigoriyalardan birimi kiriting", reply_markup=btns('ctg'))
    else:
        log['state'] = 1
        change_log(message=log, user_id=user.id)
        update.message.reply_text("Asalomu alekum Ismingizni kiriting")


def recieved_message(update, context):
    msg = update.message.text
    user = update.message.from_user
    log = to_dict(get_user_log(user.id)[0])

    if log.get('state', 0) == 1:
        log['ism'] = msg
        log['state'] = 2
        update.message.reply_text("Familyangizni kiriting")
    elif log.get('state', 0) == 2:
        log['familya'] = msg
        log['state'] = 3
        update.message.reply_text("Viloyatningizni kiriting",
                                  reply_markup=ReplyKeyboardMarkup(bts, resize_keyboard=True))

    elif log.get('state', 0) == 3:
        log['vil'] = msg
        log['state'] = 4
        update.message.reply_text("Raqamingizni kiriting",
                                  reply_markup=ReplyKeyboardMarkup(contact, resize_keyboard=True))

    elif log.get("state", 0) == 10:
        log['state'] = 11
        log['msg'] = msg
        update.message.reply_text("Categorialardan birini tanlang",
                                  reply_markup=btns(tip="ctgs", msg=msg))

    # back bn ishlash uchun
    if msg == "Back":
        state = log.get("state", 0)
        if state == 11:
            log['state'] = 10
            update.message.reply_text("Katigoriyalardan birimi kiriting", reply_markup=btns('ctg'))
        elif state == 12:
            log['state'] = 11
            update.message.reply_text("Categorialardan birini tanlang",
                                      reply_markup=btns(tip="ctgs", msg=log["msg"]))
    change_log(user.id, log)


def recived_contact(update, cotext):
    contact = update.message.contact
    user = update.message.from_user
    log = to_dict(get_user_log(user.id)[0])
    if log['state'] == 4:
        log["phone"] = contact.phone_number
        edit_user(log, user.id)
        change_log(message={"state": 10}, user_id=user.id)
        update.message.reply_text("Siz Registeratsiadan o'tingiz \n Qayta start bosing ")


def main():
    Token = "5029554294:AAG1JdSMu438pEZNqbj5J2SAbhGEDSkTyWw"
    updater = Updater(Token)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, recieved_message))
    updater.dispatcher.add_handler(MessageHandler(Filters.contact, recived_contact))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
