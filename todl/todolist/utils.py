from .models import *
import calendar
import datetime
from .models import Todo, TodoTags
from django.utils.timezone import make_aware


class DataMixin:
    """
    Class to realise DRY principe
    """

    menu = [
        {'title': 'About', 'url_name': 'about'},
        {'title': 'Login', 'url_name': 'login'},
        {'title': 'Registration', 'url_name': 'register'},
    ]

    logged_menu = [
        {'title': 'About', 'url_name': 'about'},
        {'title': 'Logout', 'url_name': 'logout'},
        {'title': 'Completed todoes', 'url_name': 'completed_todoes'},
        {'title': 'Your todoes', 'url_name': 'todoes'},
        {'title': 'Your TodoTags', 'url_name': 'edit_tags'},
        {'title': 'Calendar view', 'url_name': 'calendar_view'},
    ]

    base_tags = [
        {'tag_name': 'Task'},
        {'tag_name': 'Meeting'},
        {'tag_name': 'Work'},
        {'tag_name': 'Home'},
        {'tag_name': 'Other'},
    ]


class TodoCalendarToView:
    today = datetime.datetime.now()
    calendar_ = calendar.Calendar()
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def __init__(self, user, day=today.day, month=today.month, year=today.year):
        """
        :param user: take user object
        :param day: take required day int-number. By default == today day number
        :param month: take required month int-number. By default == current/today month number
        :param year: take required year int-number. By default == current/today year number
        """
        self.day = day
        self.month = month
        self.year = year
        self.user = user
        self.day_todoes = self.get_todoes_by_day()
        self.month_days = self.get_month_days()
        self.month_name = self.get_month_name()
        self.month_todoes = self.get_todoes_by_month()

    def get_month_days(self):
        """
        :return: list of lists with weekdays
        """
        current_month = self.calendar_.monthdayscalendar(self.year, self.month)
        return current_month

    def get_month_name(self):
        """
        :return: name of month in date
        """
        month_name = calendar.month_name[self.month]
        return month_name

    def get_todoes_by_month(self):
        """
        :return: dict in format {date of month: list of todoes-objects}
        """
        res = {}
        for date in self.calendar_.itermonthdates(year=self.year, month=self.month):
            if date.month == self.month:
                todo = Todo.objects.filter(user_id=self.user.id, timestamp_todo=date)
                day = date.day
                res[day] = todo
        return res

    def get_todoes_by_day(self):
        """
        :return: list of todoes-objects by date
        """
        date = datetime.date(self.year, self.month, self.day)
        todoes = Todo.objects.filter(user_id=self.user.id, timestamp_todo=date)
        return todoes


class AddTodo:
    """
    Class that separate part of todoes adding functional from view-classes.
    """

    def __init__(self, request, form):
        """
        :param request: django request-object from view function/class
        :param form: django form object
        """
        self.todo = None
        self.request = request
        self.form = form
        self.user = request.user

    def __get_cleaned_data(self):
        return self.form.cleaned_data

    def add_todo(self):
        cd = self.__get_cleaned_data()
        self.todo = Todo.objects.create(
            title=cd.get('title'),
            timestamp_todo=cd.get('timestamp_todo'),
            user_id=self.user.id
        )
        self.todo.save()
        self.__add_tags()

    def __add_tags(self):
        cd = self.__get_cleaned_data()
        if cd.get('tag'):
            for t in cd.get('tag'):
                tag = TodoTags.objects.filter(user_id=self.user.id).get(tag_name=t)
                self.todo.tags.add(tag)
