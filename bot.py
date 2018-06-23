# -*- coding: utf-8 -*-
import telebot
import re
import sqlite3
import os
import configparser
from telebot import types

config = configparser.ConfigParser()
config.read('config.ini')

res = ['thread', 'stick', 'pelt','bone','coal','charcoal','powder','iron ore','cloth','silver ore', \
    'magic stone', 'sapphire','solvent','ruby','hardener','steel','leather','bone powder','string', \
    'coke','rope','metal plate']
bot_token = config['USER_BOT']['BOT_TOKEN']
db_name = config['DATABASE']['DB_NAME']

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, u'To use this bot type `/line_item_days`, for example /line\_thread\_1', parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def test_func(m):
    pattern_string = '^\/line\_([A-Za-z])+\_([1-9]|[1-2]\d|30)$'
    pattern = re.compile(pattern_string)
    if pattern.match(m.text):
        arr = m.text.split('_')
        if arr[1].lower() in res:
            sendingPlot(m, arr[1], int(arr[2]))
        else:
            bot.send_message(m.chat.id, u'Sorry, i don\'t know item `%s`' % arr[1], parse_mode="Markdown")
    else:
        bot.send_message(m.chat.id, u'Not correct format `/line_item_days`\nPS: number of days is limited to 30', parse_mode="Markdown")
    pass

def sendingPlot(m, item, days):
    limit = 288 * days
    name = '%s_plot.png' % m.chat.id
    price_arr = ','.join([str(i) for i in getRes(item, limit)])
    os.system("python3 plot.py %s %s %s %s" % (name, item, price_arr, days))
    if os.path.isfile(name):
        bot.send_photo(m.chat.id, open(name, 'rb'))
        os.remove(name)
    else:
        bot.send_message(m.chat.id, u'Ooops, something wrong, try again');

def getRes(item, limit):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    result = cursor.execute('SELECT group_concat([%s], ",") FROM (SELECT [%s] FROM (SELECT * FROM Resources ORDER BY upd_time DESC LIMIT %s) ORDER BY upd_time ASC)' % (item, item, limit)).fetchone()[0]
    conn.close()
    result = result.split(',')
    return result[0::int(len(result)/96)]

if __name__ == '__main__':
    bot.infinity_polling(True)
