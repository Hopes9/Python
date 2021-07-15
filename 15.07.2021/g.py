# -*- coding: utf8 -*-

import sqlite3
import random
import telebot
from telebot import types

bot = telebot.TeleBot('')

list_ = ['К', 'Н', 'Б']  # камень, ножницы, бумага
knb_check = {'К': 'Камень', 'Н': 'Ножницы', 'Б': 'Бумага'}
whitelist = 'КНБ'


def update_db(message):

    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()

    row = cursor.execute(
        f'SELECT count_win FROM people where id = {message.from_user.id}')
    row = row.fetchall()
    if len(row) == 0:
        insert_db(message)
    else:
        update_people(message)
    print(row)
    conn.close()


def update_people(message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    cursor.execute(
        f'UPDATE people SET count_win = count_win + 1 where id = {message.from_user.id}')
    conn.commit()
    conn.close()


def insert_db(message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    name = f'{message.chat.first_name} {message.chat.last_name}'
    cursor.execute(
        f'INSERT INTO people VALUES({message.from_user.id}, "{name}", 1)')
    conn.commit()
    conn.close()


def knb(message):
    msg = message.text.lower()
    bot_knb = random.choice(list_)

    you = msg.split()[1].upper()

    if not(you in whitelist):
        return 'Введено неверное значение.'
    else:
        bot.send_message(
            message.chat.id, f'Ваш предмет: {knb_check[you]}\nПредмет бота: {knb_check[bot_knb]}')
        if bot_knb == you:
            return 'Ничья!'
        elif (bot_knb == 'К' and you == 'Б') or (bot_knb == 'Б' and you == 'Н') or (bot_knb == 'Н' and you == 'К'):
            update_db(message)
            return 'Победа!'

        else:

            return 'Поражение!'


def top_people(message):
    conn = sqlite3.connect('db.db')
    cursor = conn.cursor()
    row = cursor.execute('select name from people order by count_win desc')
    row = row.fetchall()
    print(row)
    count = 1
    top_string = ''
    for i in row:
        print(i[0])
        top_string += f'Место: {count} Имя: {i[0]}\n'
        count += 1

    return top_string


list_users_how_use = []


@bot.message_handler(commands=['rps'])
def get_text_messages(message):
    if not message.from_user.id in list_users_how_use:
        list_users_how_use.append(message.from_user.id)
        bot.send_message(
            message.chat.id, 'Добро пожаловать в Камень-Ножницы-Бумага!')
    if len(message.text.lower()) < 6:
        bot.send_message(
            message.chat.id, 'Выберите свой предмет после команды (К - камень, Н - ножницы, Б - бумага)')
    else:
        bot.send_message(message.chat.id, knb(message))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'топ':
        bot.send_message(message.chat.id, top_people(message))


bot.polling()
