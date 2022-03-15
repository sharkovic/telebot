import telebot
from ext import *
from token_set import TOKEN

bot = telebot.TeleBot(TOKEN)


def currency_withdrawal(cur_list):
    text_cur = ''
    ready_current_list = json.loads(cur_list)['results']
    for i, char in enumerate(ready_current_list, start=0):
        result = ready_current_list[f'{char}']
        text_cur += result['id'] + ' - ' + result['currencyName'] + '\n'
    return text_cur


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f"Инструкция! \n"
                                      f"Введите, через пробел, сообщение вида: \n"
                                      f"имя валюты, цену которой Вы хотите узнать \n"
                                      f"имя валюты, в которой надо узнать цену первой валюты \n"
                                      f"количество первой валюты \n"
                                      f"Например: USD RUB 200")


currency_list = currency_withdrawal(
    requests.get('https://free.currconv.com/api/v7/currencies?apiKey=269949f3c2734194ae90').content)


# Отвечает на /values

@bot.message_handler(commands=['values'])
def values_list(message):
    bot.send_message(message.chat.id, f"Доступные валюты: \n"
                                      f"\n"
                                      f" {currency_list}")


@bot.message_handler()
def converter_print(message):
    message_list = message.text.upper().split()
    try:
        if len(message_list) != 3:
            raise ErrorMessage
        elif currency_list.find(message_list[0]) == -1:
            raise FirstValueError
        elif currency_list.find(message_list[1]) == -1:
            raise SecondValueError
        elif not message_list[2].isdigit():
            raise ThirdValueError
        result = ConverterCur.get_price(message_list[0], message_list[1], int(message_list[2]))
        bot.send_message(message.chat.id, f"{round(result, 2)} {message_list[1]}")
    except ErrorMessage:
        bot.send_message(message.chat.id, f"Вы ввели запрос неверно")
    except FirstValueError:
        bot.send_message(message.chat.id, f"Вы ввели неверно имя валюты, цену которой Вы хотите узнать")
    except SecondValueError:
        bot.send_message(message.chat.id, f"Вы ввели неверно имя валюты, в которой надо узнать цену первой валюты")
    except ThirdValueError:
        bot.send_message(message.chat.id, f"Вы ввели неверно количество первой валюты")


bot.polling(none_stop=True)
