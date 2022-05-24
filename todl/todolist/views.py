from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .utils import DataMixin
from .forms import RegisterForm, LoginForm, AddingTodoForm, EditTodoForm
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
        form = AddingTodoForm()
        user = request.user
        todoes = Todo.objects.filter(user_id=user.id, status=False).order_by('-timestamp_todo')
        return render(request, self.template_name, {'menu': self.logged_menu,
                                                    'title': self.title,
                                                    'form': form,
                                                    'todoes': todoes,
                                                    'errors': errors})

    def post(self, request):
        form = AddingTodoForm(request.POST)
        user = request.user
        if form.is_valid():
            cd = form.cleaned_data
            todo = Todo.objects.create(title=cd.get('title'),
                                       timestamp_todo=cd.get('timestamp_todo'),
                                       user_id=user.id)
            todo.save()
        return self.get(request, form.errors)


class RemoveTodo(View, LoginRequiredMixin):
    def post(self, request):
        todo_id = request.POST['todo_id']
        todo = Todo.objects.get(id=todo_id)
        todo.delete()
        return redirect('todoes')


class EditTodo(View, LoginRequiredMixin, DataMixin):
    title = 'Edit todo'
    template_name = 'todolist/edit_todo.html'

    def get(self, request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        form = EditTodoForm(initial={'title': todo.title,
                                     'body': todo.body,
                                     'timestamp_todo': todo.timestamp_todo})
        return render(request, self.template_name, {'menu': self.logged_menu,
                                                    'title': self.title,
                                                    'form': form,
                                                    'todo': todo})

    def post(self, request, todo_id):
        todo_id = request.POST.get('todo_id')
        todo = Todo.objects.get(id=todo_id)
        form = EditTodoForm(request.POST)
        if form.is_valid() and form.has_changed():
            cd = form.cleaned_data
            todo.title = cd.get('title')
            todo.body = cd.get('body')
            todo.timestamp_todo = cd.get('timestamp_todo')
            todo.save()
        return redirect('todoes')


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
