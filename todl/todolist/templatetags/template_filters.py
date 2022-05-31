# coding=utf-8
from django import template

register = template.Library()


@register.filter(name='get_dict_value')
def get_dict_value(dictionary, key):
    """
    For get dict values in html-page
    :param dictionary: todolist formed by TodoCalendarToView
    :param key: int, day number
    :return: empty list or list of todoes
    """
    return dictionary.get(key)
