from django.contrib.auth import views as auth_views
from django.urls import path

from .views import profile, SignUpView, who_innovates

urlpatterns = [
    path('accounts/login/', auth_views.login, name='login'),
    path('accounts/logout/', auth_views.logout, name='logout'),
    path('accounts/sign-up/', SignUpView.as_view(), name='sign-up'),
    path('users/profile/<username>/', profile, name='profile'),
    path('users/whoinnovates/', who_innovates, name='whoinnovates'),
]
