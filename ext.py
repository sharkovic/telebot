import json
import requests


class APIException(Exception):
    pass


class ErrorMessage(APIException):
    pass


class FirstValueError(APIException):
    pass


class SecondValueError(APIException):
    pass


class ThirdValueError(APIException):
    pass


class ConverterCur:
    @staticmethod
    def get_price(cur1, cur2, quantity):
        currency_pair = f'{cur1}_{cur2}'
        res = json.loads(requests.get(
            f'https://free.currconv.com/api/v7/convert?q={currency_pair}&compact=ultra&apiKey=269949f3c2734194ae90').content)
        result = res[currency_pair] * quantity
        return result
