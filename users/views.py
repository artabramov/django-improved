from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from baskets.models import Basket
from django.core.mail import send_mail
from django.conf import settings
from users.models import User


# Create your views here.
def login(request):

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = UserLoginForm()

    context = {
        'title': 'Geekshop - Логин',
        'description': 'Описание страницы логина',
        'form': form,
    }
    return render(request, 'users/login.html', context)


def registration(request):

    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            user.set_expires()
            
            if send_key(user):
                messages.success(request, 'Registration finished.')
                return HttpResponseRedirect(reverse('users:login'))
            
            messages.error(request, 'Email sending error.')
            #return HttpResponseRedirect(reverse('users:registration'))
        else:
            print(form.errors)

    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Geekshop - Регистрация',
        'description': 'Описание страницы регистрации',
        'form': form,
    }
    return render(request, 'users/registration.html', context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Geekshop - User profile',
        'description': 'User profile description',
        #'baskets': Basket.objects.filter(user=request.user),
        'form': form,
    }
    return render(request, 'users/profile.html', context)

def confirm(request, email, auth_key):
    user = User.objects.filter(email=email, auth_key=auth_key).first()
    if user and not user.is_expired():
        user.is_active = True
        user.auth_key = ''
        user.save()
        auth.login(request, user)
    return render(request, 'users/profile.html')

def send_key(user) -> bool:
    auth_link = reverse('users:confirm', args=[user.email, user.auth_key])
    email_subject = f'auth confirm for {user.email}'
    email_body = f'click to confirm: {auth_link}'

    try:
        send_mail(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        return True

    except:
        return False


