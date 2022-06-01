from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('', IndexPage.as_view(), name='home'),
    # path('index/', IndexPage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
    path('register/', RegistrationPage.as_view(), name='register'),
    path('todoes/', TodoesPage.as_view(), name='todoes'),
    path('todoes/remove_todo/', RemoveTodo.as_view(), name='remove_todo'),
    path('todoes/done_todo/', DoneTodo.as_view(), name='done_todo'),
    path('todoes/todo/<int:todo_id>/edit_todo/', EditTodo.as_view(), name='edit_todo'),
    path('todoes/completed_todoes/', CompleteTodoesPage.as_view(), name='completed_todoes'),
    path('todoes/todo/<int:todo_id>/', TodoPage.as_view(), name='todo'),
    path('todoes/edit_tags/', EditTags.as_view(), name='edit_tags'),
    path('todoes/delete_tag/', DeleteTag.as_view(), name='delete_tag'),
    # path('todoes/by_month/<int:year>/<int:month>', CalendarView.as_view(), name='month_view'),
    path('todoes/by_day/<int:year>/<int:month>/<int:day>', DayView.as_view(), name='day_view'),
    path('todoes/calendar_view/', CalendarView.as_view(), name='calendar_view'),
    # path('todoes/day_view/', DayView.as_view(), name='day_view'),

]