"""Проект спринта №2. Калькулятор денег и калорий
Программа расчитывает деньги / калории за день(неделю)
и выводит напоминание. Версия 6.
"""

import datetime as dt
from typing import Optional


class Record:
    """Класс Record формирует записи из входных данных
    в формате количество, комментарии, дата.
    При отсутствии даты, создаёт текущую дату.
    """

    def __init__(self, amount, comment, date: Optional[str] = None):
        """Конструктор класса Record
        """
        self.amount = amount
        self.comment = comment
        self.date = date
        date_format = '%d.%m.%Y'
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()


class Calculator:
    """Класс Calculator ведет подсчёт денег(калорий)
    за день(неделю).
    """

    def __init__(self, limit):
        """Конструктор класса Calculator.
        """
        self.limit = limit
        self.records = []

    def add_record(self, notation: Record):
        """Метод add_record запрашивает данные в виде
        объекта класса Record добавляет в список records
        """
        self.records.append(notation)

    def get_today_stats(self):
        """Метод get_today_stat расчитывает сумму потраченных
        денег(калории) за текущий день
        """
        today = dt.date.today()
        sum_day = 0
        for note in self.records:
            if note.date == today:
                sum_day += note.amount
        return sum_day

    def get_week_stats(self):
        """Метод get_week_stat расчитывает сумму потраченных
        денег(калории) за текущую неделю
        """
        today = dt.date.today()
        period = dt.timedelta(days=7)
        past_day = today - period
        sum_week = 0
        for note in self.records:
            if past_day < note.date <= today:
                sum_week += note.amount
        return sum_week

    def get_balance(self):
        """Метод get_balance() выдаёт результат вычитания
        суммы денег/калорий из лимита.
        """
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    """Класс CaloriesCalculator (родительский класс -
    Calculator) для анализа калории.
    """

    def get_calories_remained(self):
        """Метод get_calories_remained запрашивает у метода
        get_balance баланс за день. В зависимости от баланса
        выводит рекомендации.
        """
        balance_calories = self.get_balance()
        if balance_calories > 0:
            return(
                "Сегодня можно съесть что-нибудь ещё, но"
                f" с общей калорийностью не более {balance_calories} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    """Класс CashCalculator (родительский класс - Calculator)
    для анализа денег.
    """
    USD_RATE = 73.16
    EURO_RATE = 86.86

    def get_today_cash_remained(self, currency):
        """Метод get_today_cash_remained запрашивает у метода
        get_balance баланс. После проверки баланса выводит
        рекомендации в той валюте, в которой запросили при
        обращении к данному методу.
        """
        cash_list = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }
        if currency not in cash_list:
            return "Данная валюта не поддерживается"
        balance_cash = self.get_balance()
        cash_name = cash_list[currency][1]
        if balance_cash == 0:
            return "Денег нет, держись"
        rounding_remainder = round((balance_cash / cash_list[currency][0]), 2)
        if balance_cash > 0:
            return f"На сегодня осталось {rounding_remainder} {cash_name}"
        rounding_remainder = abs(rounding_remainder)
        return("Денег нет, держись: твой долг - "
               f"{rounding_remainder} {cash_name}"
               )
