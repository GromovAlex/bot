import telebot
from loguru import logger
from telebot import custom_filters
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

from config.config import token, policy_branch, start_branch, gender_branch
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
    gender_page = State()

#reply_markup = generate_keyboard(start_branch)
 
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, text='Начать', reply_markup=generate_keyboard(start_branch))
    logger.info(f'Received /start message from {message.from_user.username} ({message.from_user.id})')
    user_name = message.from_user.first_name
    bot.send_message(message.chat.id, f'{user_name},{general_info}', 
                      reply_markup=generate_keyboard(policy_branch), parse_mode="HTML")
    bot.set_state(message.from_user.id, TelegramBotStates.start_page, message.chat.id)

@bot.message_handler(state=TelegramBotStates.start_page)
def start_page(message):
    try:
        match message.text:
            case 'Принять':
                bot.send_message(message.chat.id, 'Выберите пол',
                                reply_markup=generate_keyboard(gender_branch))
                bot.set_state(message.from_user.id, TelegramBotStates.gender_page, message.chat.id)
            case 'Отказаться':
                bot.send_message(message.chat.id, 'Возвращайтесь к нам, когда будете готовы!',
                                reply_markup=generate_keyboard(start_branch))
            case _:
                raise ''

    except Exception as ex:
        logger.error(ex)
        logger.info(f'Посмотреть кнопки {start_message.__name__}')
    
    finally:
        bot.send_message(message.chat.id, 'Возвращайтесь к нам, когда будете готовы!',
                                reply_markup=generate_keyboard(start_branch))
