"""Проект спринта №2. Калькулятор денег и калорий
Программа расчитывает деньги / калории за день(неделю)
и выводит напоминание.
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
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, date_format).date()
        self.spisok_record = [self.amount, self.comment, self.date]


class Calculator:
    """Класс Calculator ведет подсчёт денег(калорий)
    за день(неделю).
    """

    def __init__(self, limit):
        """Конструктор класса Calculator.
        """
        self.limit = limit
        self.records = []

    def add_record(self, spisok_record: Record):
        """Метод add_record запрашивает данные в виде списка
        от объекта класса Record и добавляет в список records
        """
        self.records.append(spisok_record)

    def get_today_stats(self):
        """Метод get_today_stat расчитывает сумму потраченных
        денег(калории) за текущий день
        """
        self.today = dt.datetime.now().date()
        self.summa_day = 0
        for i in self.records:
            if i.date == self.today:
                self.summa_day += i.amount
        return self.summa_day

    def get_week_stats(self):
        """Метод get_week_stat расчитывает сумму потраченных
        денег(калории) за текущую неделю
        """
        self.today = dt.datetime.now().date()
        self.period = dt.timedelta(days=7)
        self.past_day = self.today - self.period
        self.summa_week = 0
        for i in self.records:
            if (i.date > self.past_day) and (i.date <= self.today):
                self.summa_week += i.amount
        return self.summa_week


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
        calories_ost = self.limit - calories
        if self.limit >= calories:
            return(
                "Сегодня можно съесть что-нибудь ещё, но"
                f" с общей калорийностью не более {calories_ost} кКал")
        else:
            return("Хватит есть!")


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
        self.kurs = {'rub': 1, 'usd': self.USD_RATE, 'eur': self.EURO_RATE}
        self.names = {'rub': 'руб', 'usd': 'USD', 'eur': 'Euro'}
        self.cash = self.get_today_stats()
        self.summa = self.limit - self.cash
        self.currency = currency
        itog = round((self.summa / self.kurs[self.currency]), 2)
        if self.limit > self.cash:
            return(f"На сегодня осталось {itog} {self.names[self.currency]}")
        elif self.limit == self.cash:
            return("Денег нет, держись")
        else:
            return(
                "Денег нет, держись: твой долг"
                f" - {itog*(-1)} {self.names[self.currency]}"
            )
