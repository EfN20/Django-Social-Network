from django.urls import path
# from django.contrib.auth.views import auth_login
from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    # path('login/', auth_login, name="login"),
    path('profile/', ProfileView.as_view(), name='profile'),    
]

