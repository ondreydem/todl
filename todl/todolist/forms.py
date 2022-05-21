from django import forms
from .models import User
from django.contrib.auth import authenticate


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
    timestamp_deadline = forms.DateTimeField(label='Todo deadline',
                                             widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
