import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Словарь для хранения информации о созданных ботах
user_bots = {}

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Используйте команду /create_bot для создания нового бота.')

# Команда /create_bot
def create_bot(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_bots:
        update.message.reply_text('Вы уже создали бота.')
    else:
        bot_name = f"Bot_{user_id}"  # Имя нового бота
        user_bots[user_id] = {
            'name': bot_name,
            'messages': []
        }
        update.message.reply_text(f'Ваш бот "{bot_name}" успешно создан! Используйте команду /send_message для отправки сообщений.')

# Команда /send_message
def send_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_bots:
        update.message.reply_text('Сначала создайте бота с помощью команды /create_bot.')
        return
    
    if context.args:
        message = ' '.join(context.args)
        user_bots[user_id]['messages'].append(message)
        update.message.reply_text(f'Сообщение добавлено в ваш бот: {message}')
    else:
        update.message.reply_text('Пожалуйста, введите сообщение после команды.')

# Команда /list_messages
def list_messages(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id not in user_bots:
        update.message.reply_text('Сначала создайте бота с помощью команды /create_bot.')
        return
    
    messages = user_bots[user_id]['messages']
    if messages:
        update.message.reply_text("Ваши сообщения:\n" + "\n".join(messages))
    else:
        update.message.reply_text('У вас нет сообщений.')

# Основная функция
def main() -> None:
    # Вставьте сюда ваш токен
    TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("create_bot", create_bot))
    dispatcher.add_handler(CommandHandler("send_message", send_message))
    dispatcher.add_handler(CommandHandler("list_messages", list_messages))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
