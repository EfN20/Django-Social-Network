from django.urls import path
from .views import RegistrationView, UpdateProfile, login_view, logout_view, IndexView

app_name = 'users'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('edit/', UpdateProfile.as_view(), name='profile'),
    path('', IndexView.as_view(), name='main')
]

