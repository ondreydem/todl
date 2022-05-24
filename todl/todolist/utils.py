from .models import *
from django.shortcuts import reverse


class DataMixin:
    menu = [{'title': 'About', 'url_name': 'about'},
            {'title': 'Login', 'url_name': 'login'},
            {'title': 'Registration', 'url_name': 'register'},
            ]

    logged_menu = [{'title': 'About', 'url_name': 'about'},
                   {'title': 'Logout', 'url_name': 'logout'},
                   {'title': 'Completed todoes', 'url_name': 'completed_todoes'},
                   {'title': 'Your todoes', 'url_name': 'todoes'},
                   # {'title': 'Edit Profile', 'url_name': 'edit'},
                   ]

    base_tags = [{'tag_name': 'Task'},
                 {'tag_name': 'Meeting'},
                 {'tag_name': 'Work'},
                 {'tag_name': 'Home'}]
