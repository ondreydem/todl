from .models import *
from django.shortcuts import reverse
import calendar
import datetime


class DataMixin:
    menu = [{'title': 'About', 'url_name': 'about'},
            {'title': 'Login', 'url_name': 'login'},
            {'title': 'Registration', 'url_name': 'register'},
            ]

    logged_menu = [{'title': 'About', 'url_name': 'about'},
                   {'title': 'Logout', 'url_name': 'logout'},
                   {'title': 'Completed todoes', 'url_name': 'completed_todoes'},
                   {'title': 'Your todoes', 'url_name': 'todoes'},
                   {'title': 'Your TodoTags', 'url_name': 'edit_tags'},
                   {'title': 'Calendar view', 'url_name': 'calendar_view'}
                   # {'title': 'Edit Profile', 'url_name': 'edit'},
                   ]

    base_tags = [{'tag_name': 'Task'},
                 {'tag_name': 'Meeting'},
                 {'tag_name': 'Work'},
                 {'tag_name': 'Home'}]


class TodoCalendarToView:
    # today = datetime.datetime.today()
    calendar_ = calendar.Calendar()

    def __init__(self, user, today):
        """
        :param user: take a current user object
        """
        self.today = today
        self.user = user
        self.month_days = self.get_month_by_today()
        self.day_number = 0
        self.days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.month_name = self.get_month_name()
        self.year = self.today.year
        self.month = self.today.month
        self.month_todoes = self.get_todoes_by_date()



    def get_month_by_today(self):
        """
        :return: list of lists with weekdays
        """
        current_month = self.calendar_.monthdayscalendar(self.today.year, self.today.month)
        return current_month

    def get_month_name(self):
        """
        :return: name of month in date
        """
        month_name = calendar.month_name[self.today.month]
        return month_name

    def get_todoes_by_date(self):
        """
        :param date: datetime.date object
        :return: dict in format {date of month: list of todoes}
        """
        res = {}
        for date in self.calendar_.itermonthdates(year=self.year, month=self.month):
            if date != 0:
                day = date.day
                todo = Todo.objects.filter(user_id=self.user.id, timestamp_todo=date).all()
                res[day] = todo
        return res

    # context = {
    #     'current_month': self.get_month_by_today(),
    #     'today_number': self.today.day,
    #     'header': self.days_of_the_week,
    #     'month_name': self.get_month_name(self.today.month),
    #     'current_year': self.today.year
    # }
