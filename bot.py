import telebot
import sqlite3

TOKEN = '8120368501:AAExhvrjc1yCyCzDbNglpo0sgDSM8eIxPL0'

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect('Пользователи.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Пользователи (
    id INTEGER PRIMARY KEY,
    name TEXT
)''')


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id

    cursor.execute('SELECT name FROM Пользователи WHERE id = ?',(user_id,))
    result = cursor.fetchone()

    if result is None:
        bot.send_message(message.chat.id, "Привет! Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        name = result[0]
        bot.send_message(message.chat.id, f"Привет, {name}!")

def get_name(message):
    user_id = message.from_user.id
    name = message.text


    cursor.execute("INSERT INTO Пользователи (id, name) VALUES (?, ?)", (user_id, name))
    conn.commit()

    bot.send_message(message.chat.id, f"Отлично! Теперь ты зарегестрирован, {name}!")
conn.commit()
bot.polling(none_stop=True)
