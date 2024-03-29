from django.urls import path
from users.views import login, registration, logout, profile, confirm

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('confirm/<str:email>/<str:auth_key>', confirm, name='confirm'),
]
