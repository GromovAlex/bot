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
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in buttons_list:
        button = KeyboardButton(option)
        keyboard.add(button)
    return keyboard

class TelegramBotStates(StatesGroup):
    start_page = State()
    agreement_page = State()
    gender_page = State()
    params = State()

 

@bot.message_handler(commands=['start'])
def start(message):
    logger.info(f'Received /start message from {message.from_user.username} ({message.from_user.id})')
    bot.send_message(message.chat.id, 'Добро пожаловать',
                                reply_markup=generate_keyboard(start_branch))
    bot.set_state(message.from_user.id, TelegramBotStates.start_page, message.chat.id)


@bot.message_handler(state=TelegramBotStates.start_page)
def start_page(message):
    match message.text:
        case 'Начать' :
            user_name = message.from_user.first_name
            bot.send_message(message.chat.id, f'{user_name},{general_info}', 
                                    reply_markup=generate_keyboard(policy_branch), parse_mode="HTML")
            bot.set_state(message.from_user.id, TelegramBotStates.agreement_page, message.chat.id)


@bot.message_handler(state=TelegramBotStates.agreement_page)
def agreement_page(message):  
    try:
        match message.text:
            case 'Принять':
                bot.send_message(message.chat.id, 'Выберите пол',
                                reply_markup=generate_keyboard(gender_branch))
                bot.set_state(message.from_user.id, TelegramBotStates.gender_page, message.chat.id)
            case 'Отказаться':
                bot.send_message(message.chat.id, 'Возвращайтесь к нам, когда будете готовы!',
                                reply_markup=generate_keyboard(start_branch))
                bot.set_state(message.from_user.id, TelegramBotStates.start_page, message.chat.id)
            case _:
                raise ''
    
    except Exception as ex:
        logger.error(ex)
        logger.info(f'Введено сообщение не с кнопки {start_message.__name__}')
        bot.send_message(message.chat.id, 'Введите сообщение с кнопки',
                                reply_markup=generate_keyboard(policy_branch))
        bot.set_state(message.from_user.id, TelegramBotStates.start_page, message.chat.id)

@bot.message_handler(state=TelegramBotStates.gender_page)
def gender_page(message):
    keyboard = ReplyKeyboardRemove()
    match message.text:
        case 'Мужской':
            bot.send_message(message.chat.id, 'Введите ваш возраст(только цифру)', reply_markup=keyboard)
            bot.set_state(message.from_user.id, TelegramBotStates.params, message.chat.id)

        case 'Женский':
            bot.send_message(message.chat.id, 'Введите ваш возраст(только цифру)', reply_markup=keyboard)
            bot.set_state(message.from_user.id, TelegramBotStates.params, message.chat.id)

@bot.message_handler(content_types=["text"], state=TelegramBotStates.params)
def process_age_step(message):
    try:
        age = int(message.text)
        msg = bot.send_message(message.chat.id, 'Введите ваш рост(только цифру)')
        bot.register_next_step_handler(msg, process_height_step, age) 
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите возраст цифрами.')
        bot.register_next_step_handler(message, process_age_step)

def process_height_step(message, age): 
    try:
        height = int(message.text)
        msg = bot.send_message(message.chat.id, 'Введите ваш вес(только цифру)')
        bot.register_next_step_handler(msg, process_weight_step, height, age)  
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите рост цифрами.')
        bot.register_next_step_handler(message, process_height_step, age) 

def process_weight_step(message, height, age):  
    try:
        weight = int(message.text)
        bot.send_message(message.chat.id, f'Ваш возраст: {age}, Рост: {height}, Вес: {weight}')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите вес цифрами.')
        bot.register_next_step_handler(message, process_weight_step, height, age)        
