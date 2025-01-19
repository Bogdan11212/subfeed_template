import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Словарь для хранения созданных ботов
user_bots = {}

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Используй команду /create_bot для создания своего бота.')

# Команда /create_bot
def create_bot(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_bots:
        update.message.reply_text('Вы уже создали бота. Используйте команду /send_message для отправки сообщений.')
    else:
        user_bots[user_id] = []
        update.message.reply_text('Ваш бот успешно создан! Используйте команду /send_message для отправки сообщений.')

# Команда /send_message
def send_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_bots:
        update.message.reply_text('Сначала создайте бота с помощью команды /create_bot.')
        return
    
    if context.args:
        message = ' '.join(context.args)
        user_bots[user_id].append(message)
        update.message.reply_text(f'Сообщение добавлено: {message}')
    else:
        update.message.reply_text('Пожалуйста, введите сообщение после команды.')

# Основная функция
def main() -> None:
    # Вставьте сюда ваш токен
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("create_bot", create_bot))
    dispatcher.add_handler(CommandHandler("send_message", send_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
