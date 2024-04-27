from django.urls import path
from .views import *



urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/user/', CurrentUserView.as_view()),
    path('register/', CustomRegisterView.as_view()),
    path('login/', UserLoginView.as_view()),

]