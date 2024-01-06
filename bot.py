import telebot
import logging
from telebot import custom_filters
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

from config.config import token, start_branch
from msn.message import general_info


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token, state_storage=state_storage)
bot.add_custom_filter(custom_filters.StateFilter(bot))

def run():
    bot.infinity_polling()


def generate_keyboard(buttons_list: list):
    keyboard = ReplyKeyboardMarkup()
    for option in buttons_list:
        keyboard.add(InlineKeyboardButton(text=option, callback_data=option))
    return keyboard

class TelegramBotStates(StatesGroup):
    start_page = State()
 
@bot.message_handler(commands=['start'])
def start_message(message):
    logging.info(f'Received /start message from {message.from_user.username} ({message.from_user.id})')
    bot.send_message(message.chat.id, general_info, reply_markup=generate_keyboard(start_branch))
    bot.set_state(message.from_user.id, TelegramBotStates.start_page, message.chat.id)

@bot.message_handler(state=TelegramBotStates.start_page)
def start_page(message):
    match message.text:
        case _:
            'pass'