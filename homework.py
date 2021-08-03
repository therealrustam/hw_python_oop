"""Проект спринта №2. Калькулятор денег и калорий
Программа расчитывает деньги / калории за день(неделю)
и выводит напоминание. Версия 2.
"""

import datetime as dt
from typing import Optional


class Record:
    """Класс Record формирует список из входных данных
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
        self.record_list = [self.amount, self.comment, self.date]


class Calculator:
    """Класс Calculator ведет подсчёт денег(калорий)
    за день(неделю).
    """

    def __init__(self, limit):
        """Конструктор класса Calculator.
        """
        self.limit = limit
        self.records = []

    def add_record(self, record_list: Record):
        """Метод add_record запрашивает данные в виде списка
        от объекта класса Record и добавляет в список records
        """
        self.records.append(record_list)

    def get_today_stats(self):
        """Метод get_today_stat расчитывает сумму потраченных
        денег(калории) за текущий день
        """
        today = dt.date.today()
        sum_day = 0
        for note in self.records:
            if note.date == today:
                sum_day += note.amount
        self.balance = self.limit - sum_day
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


class CaloriesCalculator(Calculator):
    """Класс CaloriesCalculator (родительский класс -
    Calculator) для анализа калории.
    """

    def get_calories_remained(self):
        """Метод get_calories_remained запрашивает у метода
        get_today_stats сумму калорий за день и ограничение.
        После сравнения данных параметров выводит рекомендации.
        """
        calories = self.get_today_stats()
        if self.limit >= calories:
            return(
                "Сегодня можно съесть что-нибудь ещё, но"
                f" с общей калорийностью не более {self.balance} кКал")
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
        get_today_stats сумму потраченных денег за день и ограничение.
        После сравнения данных параметров выводит рекомендации в той валюте,
        в которой запросили при обращении к данному методу.
        """
        cash_list = {
            'rub': (1, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }
        cash = self.get_today_stats()
        self.currency = currency
        if self.balance != 0:
            rounding_remainder = round(
                (self.balance / cash_list[self.currency][0]), 2)
        if self.currency not in cash_list.keys():
            return "Данная валюта не поддерживается"
        else:
            if self.limit > cash:
                return(
                    f"На сегодня осталось {rounding_remainder}"
                    f" {cash_list[self.currency][1]}"
                )
            elif self.limit == cash:
                return "Денег нет, держись"
            else:
                return(
                    "Денег нет, держись: твой долг"
                    f" - {abs(rounding_remainder)}"
                    f" {cash_list[self.currency][1]}"
                )
