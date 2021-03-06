import datetime

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .utils import DataMixin, TodoCalendarToView, AddTodo
from .forms import RegisterForm, LoginForm, AddingTodoForm, EditTodoForm, CreateTagForm
from .models import User, Todo, TodoTags


# Create your views here.


class IndexPage(View, DataMixin):
    template = 'todolist/index.html'
    title = 'Mainpage'

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template, {'title': self.title,
                                                   'menu': self.logged_menu})
        return render(request, self.template, {'title': self.title,
                                               'menu': self.menu})


class AboutPage(View, DataMixin):
    pass


class LoginPage(View, DataMixin):
    template_name = 'todolist/login.html'
    title = 'Login page'

    def get(self, requset, *errors):
        form = LoginForm()
        if not errors:
            return render(requset, self.template_name, {'form': form,
                                                        'title': self.title,
                                                        'menu': self.menu})
        else:
            return render(requset, self.template_name, {'form': form,
                                                        'menu': self.menu,
                                                        'errors': errors})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            login(request, user)
            return redirect('todoes')
        else:
            return self.get(request, form.errors)


class LogoutPage(View, DataMixin, LoginRequiredMixin):

    def get(self, request):
        logout(request)
        return redirect('login')


class RegistrationPage(View, DataMixin):
    template_name = 'todolist/register.html'
    title = 'Registration page'

    def get(self, request, errors=None):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form,
                                                    'menu': self.menu,
                                                    'title': self.title,
                                                    'errors': errors})

    def post(self, requset):
        form = RegisterForm(requset.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'],
                                            email=cd['email'],
                                            password=cd['password'])
            user.save()
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                for tag in self.base_tags:
                    base_tags = TodoTags.objects.create(tag_name=tag.get('tag_name'), user_id=user)
                login(requset, user)
                return redirect(reverse('todoes'))
            else:
                msg = 'Something went wrong, please try again'
                return self.get(requset, errors=msg)
        else:
            return self.get(requset, form.errors)


class TodoesPage(View, DataMixin, LoginRequiredMixin):
    template_name = 'todolist/todoes.html'
    title = 'Todoes page'

    def get(self, request, errors=None):
        form = AddingTodoForm(user=request.user)
        user = request.user
        todoes = Todo.objects.filter(user_id=user.id, status=False).order_by('timestamp_todo')
        return render(request, self.template_name, {'menu': self.logged_menu,
                                                    'title': self.title,
                                                    'form': form,
                                                    'todoes': todoes,
                                                    'errors': errors})

    def post(self, request):
        form = AddingTodoForm(request.POST, user=request.user)
        add_todo = AddTodo(request, form)
        if form.is_valid():
            add_todo.add_todo()
        return self.get(request, errors=form.errors)


class RemoveTodo(View, LoginRequiredMixin):
    def post(self, request):
        todo_id = request.POST.get('todo_id')
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return redirect('todoes')


class EditTodo(View, LoginRequiredMixin, DataMixin):
    title = 'Edit todo'
    template_name = 'todolist/edit_todo.html'

    def get(self, request, todo_id, errors=None):
        todo = Todo.objects.get(id=todo_id)
        tags = [tag.tag_name for tag in todo.tags.all()]
        form = EditTodoForm(user=request.user,
                            initial={'title': todo.title,
                                     'body': todo.body,
                                     'timestamp_todo': todo.timestamp_todo,
                                     'tag': tags})
        return render(request, self.template_name, {'menu': self.logged_menu,
                                                    'title': self.title,
                                                    'form': form,
                                                    'todo': todo,
                                                    'errors': errors})

    def post(self, request, todo_id):
        todo_id = request.POST.get('todo_id')
        todo = Todo.objects.get(id=todo_id)
        form = EditTodoForm(request.POST, user=request.user)
        if form.is_valid():
            cd = form.cleaned_data
            for tag in TodoTags.objects.filter(user_id=request.user.id):
                if tag.tag_name in cd.get('tag'):
                    todo.tags.add(tag)
                else:
                    todo.tags.remove(tag)
            todo.title = cd.get('title')
            todo.body = cd.get('body')
            todo.timestamp_todo = cd.get('timestamp_todo')
            todo.save()
            return redirect('todoes')
        return self.get(request, todo_id, errors=form.errors)


class DoneTodo(View, LoginRequiredMixin):
    def post(self, request):
        todo_id = request.POST['todo_id']
        todo = Todo.objects.get(id=todo_id)
        todo.status = True
        todo.timestamp_done = timezone.now()
        todo.save()
        return redirect('todoes')


class TodoPage(View, DataMixin, LoginRequiredMixin):
    template_name = 'todolist/todo.html'
    title = 'Todo page'

    def get(self, requset, todo_id):
        todo = Todo.objects.get(id=todo_id)
        return render(requset, self.template_name, {'menu': self.logged_menu,
                                                    'title': self.title,
                                                    'todo': todo})


class CompleteTodoesPage(View, DataMixin, LoginRequiredMixin):
    template_name = 'todolist/complete_todoes.html'
    title = 'Complete todoes'

    def get(self, request):
        compl_todoes = Todo.objects.filter(user_id=request.user.id, status=True).order_by('-timestamp_done')
        return render(request, self.template_name, {'menu': self.logged_menu,
                                                    'title': self.title,
                                                    'todoes': compl_todoes})


class EditTags(View, DataMixin, LoginRequiredMixin):
    template_name = 'todolist/edit_tags.html'
    title = 'Edit tags'

    def get(self, request):
        form = CreateTagForm()
        tags = TodoTags.objects.filter(user_id=request.user.id)
        return render(request, self.template_name, {'menu': self.logged_menu,
                                                    'title': self.title,
                                                    'form': form,
                                                    'tags': tags})

    def post(self, request):
        form = CreateTagForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            tag = TodoTags.objects.create(tag_name=cd.get('tag_name'), user_id=request.user)
            tag.save()
            return self.get(request)


class DeleteTag(View, LoginRequiredMixin):
    def post(self, request):
        tag_id = request.POST.get('tag_id')
        tag = TodoTags.objects.get(id=tag_id)
        tag.delete()
        return redirect('edit_tags')


class CalendarView(View, LoginRequiredMixin, DataMixin):
    template_name = 'todolist/month_view.html'
    title = 'Calendar view'
    today = datetime.datetime.today()

    def get(self, request):
        if request.GET.get('month'):
            month = int(request.GET.get('month'))
            year = int(request.GET.get('year'))
            todo_by_month = TodoCalendarToView(user=request.user,
                                               year=year,
                                               month=month,
                                               day=1)
            return render(request, self.template_name, {'menu': self.logged_menu,
                                                        'title': self.title,
                                                        'todo_calendar': todo_by_month})
        todo_by_month = TodoCalendarToView(user=request.user)
        return render(request, self.template_name, {'menu': self.logged_menu,
                                                    'title': self.title,
                                                    'todo_calendar': todo_by_month})


class WeekView(View, LoginRequiredMixin, DataMixin):
    pass


class DayView(View, LoginRequiredMixin, DataMixin):
    template_name = 'todolist/day_view.html'
    title = 'Day view'

    def get(self, request, year, month, day, errors=None):
        form = AddingTodoForm(user=request.user, initial={'timestamp_todo': datetime.date(year, month, day)})
        todo_by_day = TodoCalendarToView(user=request.user, year=year, month=month, day=day)
        return render(request, self.template_name, {'todo_by_day': todo_by_day,
                                                    'menu': self.logged_menu,
                                                    'title': self.title,
                                                    'form': form,
                                                    'errors': errors})

    def post(self, request, year, month, day):
        form = AddingTodoForm(request.POST, user=request.user)
        add_todo = AddTodo(request, form)
        if form.is_valid():
            add_todo.add_todo()
        return self.get(request, year, month, day, errors=form.errors)
