from django import forms
from .models import User, TodoTags
from django.contrib.auth import authenticate
import datetime


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    username = forms.CharField(label='Username',
                               max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password',
                               min_length=4,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             required=True)

    def clean(self):
        cd = super(RegisterForm, self).clean()
        if cd.get('password') != cd.get('password2'):
            msg = 'Passwords must match!'
            self.add_error('password', msg)
        exist_user = User.objects.filter(username=cd.get('username'))
        if len(exist_user) > 0:
            msg = 'User with this username is already exist'
            self.add_error('username', msg)
        return cd


class LoginForm(forms.Form):
    username = forms.CharField(label='Login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cd = super(LoginForm, self).clean()
        current_user = authenticate(username=cd.get('username'),
                                    password=cd.get('password'))
        if current_user is None:
            exist_user = User.objects.filter(username=cd.get('username'))
            if len(exist_user) < 1:
                msg = "User with this username is doesn't exist"
                self.add_error('username', msg)
            else:
                msg = "Wrong password"
                self.add_error('password', msg)
        return cd


class AddingTodoForm(forms.Form):
    title = forms.CharField(label='Title',
                            max_length=200,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    timestamp_todo = forms.DateField(label='Todo deadline',
                                     required=True,
                                     widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
    tag = forms.MultipleChoiceField(label='Choose tags',
                                    required=False,
                                    widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        tags = [(tag.tag_name, tag.tag_name) for tag in TodoTags.objects.filter(user_id=self.user.id)]
        self.fields['tag'].choices = tags

    def clean(self):
        cd = super(AddingTodoForm, self).clean()
        if cd.get('timestamp_todo') < datetime.date.today():
            msg = "You can't add a todo to the past"
            self.add_error('timestamp_todo', msg)
        return cd


class EditTodoForm(forms.Form):
    title = forms.CharField(label='Title',
                            max_length=200,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label='Description',
                           max_length=2000,
                           required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control'}))
    timestamp_todo = forms.DateTimeField(label='Todo deadline',
                                         widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
    tag = forms.MultipleChoiceField(label='Choose tags',
                                    required=False,
                                    widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        tags = [(tag.tag_name, tag.tag_name) for tag in TodoTags.objects.filter(user_id=self.user.id)]
        self.fields['tag'].choices = tags


class CreateTagForm(forms.Form):
    tag_name = forms.CharField(label='Tag name', widget=forms.TextInput(attrs={'class': 'form-control'}))
