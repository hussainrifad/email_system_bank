from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.UserUpdateView.as_view(), name='profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logOut, name='logout')
]