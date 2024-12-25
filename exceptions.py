class CurrencyConverterException(Exception):
    pass

class InvalidFormatException(CurrencyConverterException):
    def __str__(self):
        return "Неправильный формат. Пожалуйста, используйте формат: <валюта_для_конвертации> <валюта_для_конверсии> <количество_валюты>."

class InvalidCurrencyException(CurrencyConverterException):
    def __init__(self, currency, currency_dict):
        self.currency = currency
        self.currency_dict = currency_dict

    def __str__(self):
        return f"Валюта '{self.currency}' не поддерживается. Доступные валюты: {', '.join(self.currency_dict.keys())} или их коды."

class InvalidAmountException(CurrencyConverterException):
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f"Неверное количество валюты: '{self.amount}'. Пожалуйста, введите корректное число."

class CurrencyNotFoundException(CurrencyConverterException):
    def __str__(self):
        return "Ошибка при получении данных с API: не удалось найти валюту."

class APIConnectionException(CurrencyConverterException):
    def __init__(self, error_message):
        self.error_message = error_message

    def __str__(self):
        return f"Ошибка соединения с API: {self.error_message}"