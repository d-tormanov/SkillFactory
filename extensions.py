import requests
from exceptions import *


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f'https://api.exchangerate-api.com/v4/latest/{base}'

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                raise CurrencyNotFoundException()

            if quote not in data['rates']:
                raise InvalidCurrencyException(quote)

            conversion_rate = data['rates'][quote]
            return round(amount * conversion_rate, 2)

        except requests.exceptions.RequestException as e:
            raise APIConnectionException(e)
        except KeyError:
            raise CurrencyNotFoundException()
        except Exception as e:
            raise CurrencyConverterException(f"Неизвестная ошибка: {e}")

    @staticmethod
    def is_valid_amount(amount: str) -> bool:

        try:
            value = float(amount)

            if value <= 0:
                return False

            return True
        except ValueError:
            return False
