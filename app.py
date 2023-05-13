import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConvertor


bot = telebot.TeleBot(TOKEN)

# base_ticker, quote_ticker = keys[base], keys[quote]


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f'Здравствуйте, {message.chat.username}! Я - бот-помощник, помогаю конвертировать указанную вами валюту \
в другую, используя актуальный курс на текущую дату.\n' \
f'Для начала работы введите данные в следующем формате: \n' \
f' <имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n' \
f'Нажмите /values чтобы увидеть список доступных валют.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = f'Доступные для конвертации валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введено неверное количество параметров.\n'
                                      'Пример для ввода: доллар рубль 1')

        base, quote, amount = values
        total_quote = CurrencyConvertor.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} равна - {total_quote}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
