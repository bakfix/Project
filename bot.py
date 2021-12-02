import telebot
from telebot import types
import sqlite3

TOKEN = '1985117030:AAHGKQ9Hp8W7RFbKoiQoFYkoyrAjfmKfA0o'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    order_button = types.KeyboardButton('Заказы')
    support = types.KeyboardButton('Техническая поддержка')
    reviews = types.KeyboardButton('Отзывы')
    a_service = types.KeyboardButton('О сервисе')
    markup.add(order_button, support, reviews, a_service)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def another(message):
    if message.text == "Отзывы":
        markup = types.InlineKeyboardMarkup()
        reviews_button = types.InlineKeyboardButton(text='Канал с отзывами', url='https://t.me/Studieess')
        markup.add(reviews_button)
        bot.send_message(message.chat.id, "Нажми на кнопку и перейди на канал с отзывами", reply_markup=markup)
    elif message.text == "О сервисе":
        markup = types.InlineKeyboardMarkup()
        reviews_button = types.InlineKeyboardButton(text='Как работает сервис?',
                                                    url='https://telegra.ph/O-rabote-servisa-09-28')
        markup.add(reviews_button)
        bot.send_message(message.chat.id, "Здесь можно прочитать о работе с сервисом", reply_markup=markup)
    elif message.text == "Заказы":
        keyboard_subcategory = types.ReplyKeyboardMarkup(resize_keyboard=True)
        order = types.KeyboardButton('Оформить заказ')
        do_ex = types.KeyboardButton('Выполнить заказ')
        back = types.KeyboardButton('Назад')
        keyboard_subcategory.add(order, do_ex, back)
        bot.send_message(message.chat.id, 'Выберите то, что вам нужно'.format(message.from_user),
                         reply_markup=keyboard_subcategory)
    elif message.text == "Оформить заказ":
        keyboard_orders = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_orders = types.KeyboardButton('Назад')
        form = types.KeyboardButton('Заполнить форму заказа')
        cancellation = types.KeyboardButton('Отменить заказ')
        keyboard_orders.add(form, cancellation, back_orders)
        bot.send_message(message.chat.id, 'Выберите то, что вам нужно'.format(message.from_user),
                         reply_markup=keyboard_orders)
    elif message.text == "Заполнить форму заказа":
        bot.send_message(message.chat.id, "Заполните форму заказа:\n"
                                                 "1. Предмет и описание задачи\n"
                                                 "2. Сроки выполнения работы\n"
                                                 "3. Примечание (если необходимо)\n")
        bot.register_next_step_handler(message, orders)
        # get_text_messages(message)
    elif message.text == "Выполнить заказ":
        conn = sqlite3.connect("db_test.db")
        cursor = conn.cursor()
        sql = 'SELECT id FROM orders_user'
        res = cursor.execute(sql).fetchall()
        keyboard_orders = types.ReplyKeyboardMarkup(resize_keyboard=True)
        form = types.KeyboardButton('Выбрать заказ')
        cost = types.KeyboardButton('Предложить цену')
        end = types.KeyboardButton('Завершить заказ')
        back_orders = types.KeyboardButton('Назад')
        keyboard_orders.add(form, cost, end, back_orders)
        bot.send_message(message.chat.id, f'Список активных заказов:\nВсего заказов {len(res)}',
                         reply_markup=keyboard_orders)
    elif message.text == "Назад":
        menu(message)

def orders(message):
    lst_message = message.text.split('\n')
    conn = sqlite3.connect("db_test.db")
    cursor = conn.cursor()
    query = 'INSERT INTO orders_user (id, item, timing, note) VALUES (?,?,?,?)'
    val = (message.from_user.id,lst_message[0],lst_message[1],lst_message[2])
    cursor.execute(query, val)
    conn.commit()
    cursor.close()
    conn.close()
    bot.send_message(message.chat.id, f'Ваш заказ успешно записан!')


bot.polling(none_stop=True)