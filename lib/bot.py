import telebot
from lib.config import Config


class Bot:
    def __init__(self):
        self.token = Config().bot_token
        self.chat_id = Config().bot_chat_id
        self.bot = telebot.TeleBot(self.token)

    def send_message(self, message):
        self.bot.send_message(self.chat_id, message, disable_notification=True)
