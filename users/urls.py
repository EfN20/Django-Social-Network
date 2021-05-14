from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('edit/', UpdateProfile.as_view(), name='profile_edit'),
    path('', IndexView.as_view(), name='main'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('friends/accept/<int:request_id>', accept_friend_request, name='accept_friend'),
    path('friends/send/<int:user_to>', send_friend_request, name='send_friend')
]

