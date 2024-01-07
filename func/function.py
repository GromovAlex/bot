
import telebot
from bot import bot
def process_age_step(message):
    try:
        age = int(message.text)  # Преобразуем текст в целое число
        msg = bot.send_message(message.chat.id, 'Введите ваш рост(только цифру)')
        bot.register_next_step_handler(msg, process_height_step)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите возраст цифрами.')
        bot.register_next_step_handler(message, process_age_step)

def process_height_step(message):
    try:
        height = int(message.text)
        msg = bot.send_message(message.chat.id, 'Введите ваш вес(только цифру)')
        bot.register_next_step_handler(msg, process_weight_step)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите рост цифрами.')
        bot.register_next_step_handler(message, process_height_step)

def process_weight_step(message):
    try:
        weight = int(message.text)
        # Здесь вы можете продолжать логику бота или обрабатывать введенные данные
        bot.send_message(message.chat.id, f'Ваш возраст: {age}, Рост: {height}, Вес: {weight}')
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите вес цифрами.')
        bot.register_next_step_handler(message, process_weight_step)



'''list_ans = []

list_questions = [
    'Введите ваш возраст(только цифру)', 
    'Введите ваш рост(только цифру)', 
    'Введите ваш вес(только цифру)'
                ]

def func():
    bot.send_message(message.chat.id, item, reply_markup=keyboard)
    ans = massege.text
    list_ans.append(ans)
    bot.register_next_step_handler(ans, func)

    params = {
        'age': list_ans[0], 
        'height': list_ans[1], 
        'mass': list_ans[2]
                }
    return params'''



