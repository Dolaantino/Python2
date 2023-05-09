import sqlite3
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.error import InvalidToken
# Функция-обработчик команды /start
def start(update, context):
    reply_markup = ReplyKeyboardMarkup([['/set', '/get', '/del']])
    update.message.reply_text('Привет! Я бот для хранения паролей. Чем могу помочь?', reply_markup=reply_markup)

# Функция-обработчик команды /set
def set_password(update, context):
    user_id = update.message.from_user.id
    service = update.message.text.split()[1]
    password = update.message.text.split()[2]

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    c.execute("INSERT INTO passwords (user_id, service, password) VALUES (?, ?, ?)",
              (user_id, service, password))
    conn.commit()
    conn.close()

    update.message.reply_text('Пароль успешно сохранен!')

# Функция-обработчик команды /get
def get_password(update, context):
    user_id = update.message.from_user.id
    service = update.message.text.split()[1]

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    c.execute("SELECT password FROM passwords WHERE user_id = ? AND service = ?", (user_id, service))
    result = c.fetchone()
    conn.close()

    if result:
        update.message.reply_text(f'Пароль для сервиса {service}: {result[0]}')
    else:
        update.message.reply_text(f'Пароль для сервиса {service} не найден.')

# Функция-обработчик команды /del
def delete_password(update, context):
    user_id = update.message.from_user.id
    service = update.message.text.split()[1]

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()

    c.execute("DELETE FROM passwords WHERE user_id = ? AND service = ?", (user_id, service))
    conn.commit()
    conn.close()

    update.message.reply_text(f'Пароль для сервиса {service} успешно удален.')

# Функция-обработчик неизвестных команд
def unknown_command(update, context):
    update.message.reply_text('Неизвестная команда.')

# Функция-обработчик текстовых сообщений
def handle_message(update, context):
    update.message.reply_text('Я понимаю только команды /set, /get и /del.')

def main():
    # Инициализация базы данных
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (user_id INTEGER, service TEXT, password TEXT)''')
    conn.commit()
    conn.close()

    # Инициализация бота
    try:
        updater = Updater('5971377605:AAG2KmULVonGguVbexBxwUlvxafz2zgqdSA')

    # Получение диспетчера обновлений
        dp = updater.dispatcher

    # Регистрация обработчиков команд
        dp.add_handler(CommandHandler('start', start))
        dp.add_handler(CommandHandler('set', set_password))
        dp.add_handler(CommandHandler('get', get_password))
        dp.add_handler(CommandHandler('del', delete_password))

    # Регистрация обработчиков неизвестных команд и текстовых сообщений
        dp.add_handler(MessageHandler(Filters.command, unknown_command))
        dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Запуск бота
        updater.start_polling()
        updater.idle()

    except InvalidToken:
            print("Invalid bot token. Please check your bot token and try again.")

if __name__ == '__main__':
    main()
