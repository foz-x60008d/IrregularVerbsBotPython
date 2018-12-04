import argparse
import logging
from typing import Dict

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from bot.classes import TrainSession, Word

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# текущие упражнения по id чата
train_sessions_db: Dict[int, TrainSession] = dict()


def start(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Будем тренироваться?\nНабери /train для начала тренировки"
    )


def train(bot, update):
    if update.message.chat_id not in train_sessions_db:
        train_sessions_db[update.message.chat_id] = TrainSession(
            [Word('do', 'did', 'done'), Word('set', 'set', 'set')]
        )

    bot.send_message(
        chat_id=update.message.chat_id,
        text=train_sessions_db[update.message.chat_id].ask()
    )


def answer(bot, update):
    if update.message.chat_id not in train_sessions_db:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="Будем тренироваться?\nНабери /train для начала тренировки"
        )
        return

    result = train_sessions_db[update.message.chat_id].check_answer(update.message.text)
    message = "Все верно!" if result else "Не верно!"

    if train_sessions_db[update.message.chat_id].finished:
        message += "\nТренировка завершена."
        del train_sessions_db[update.message.chat_id]
    else:
        message += "\n" + train_sessions_db[update.message.chat_id].ask()

    bot.send_message(
        chat_id=update.message.chat_id,
        text=message
    )


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='token')
    args = parser.parse_args()

    updater = Updater(token=args.token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    train_handler = CommandHandler('train', train)
    dispatcher.add_handler(train_handler)

    answer_handler = MessageHandler(Filters.text, answer)
    dispatcher.add_handler(answer_handler)

    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()
