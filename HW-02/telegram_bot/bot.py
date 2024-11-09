from telebot import TeleBot, types
from config import TOKEN, currencies
from extensions import CurrencyConverter
from exceptions import *

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: types.Message):
    text = "Введите запрос в формате:\n\
<валюта_для_конвертации> <валюта_для_конверсии> <количество_валюты>\
\nНапример: USD EUR 10 (доллар евро 10)\
\nИспользуй команду /values для получения доступных валют."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def send_values(message: types.Message):
    text = 'Доступные валюты:'
    for currency in currencies:
        text += f'\n - {currency} ({currencies[currency]})'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def handle_text(message: types.Message):
    try:
        text = message.text.split()
        currencies_rev = {value: key for key, value in currencies.items()}

        if len(text) != 3:
            raise InvalidFormatException()

        base_name, quote_name, amount = text
        if not CurrencyConverter.is_valid_amount(amount):
            raise InvalidAmountException(amount)

        amount = float(amount)

        if base_name in currencies:
            base_code = currencies[base_name]
        elif base_name.upper() in currencies_rev:
            base_code = base_name.upper()
        else:
            raise InvalidCurrencyException(base_name, currencies)

        if quote_name in currencies:
            quote_code = currencies[quote_name]
        elif quote_name.upper() in currencies_rev:
            quote_code = quote_name.upper()
        else:
            raise InvalidCurrencyException(quote_name, currencies)

        result = CurrencyConverter.get_price(base_code, quote_code, amount)
        bot.send_message(message.chat.id, f"{amount} {base_name.upper()} = {result} {quote_name.upper()}")

    except CurrencyConverterException as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")


if __name__ == '__main__':
    bot.infinity_polling()