from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from users.models import User, UserProfile

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя',
    }))

    password = forms.CharField(widget=PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль',
    }))
    
    class Meta:
        model = User
        fields = 'username', 'password'


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя',
    }))

    email = forms.CharField(widget=EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите адрес эл. почты',
    }))

    first_name = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя',
    }))

    last_name = forms.CharField(widget=TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите фамилию',
    }))

    password1 = forms.CharField(widget=PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль',
    }))

    password2 = forms.CharField(widget=PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Подтвердите пароль',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 
        'readonly': True}))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 
        'readonly': True}))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'image')

class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('tags', 'bio', 'gender')

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
