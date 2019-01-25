from django.contrib.auth import views as auth_views
from django.urls import path

from .views import profile, SignUpView, login, who_innovates, set_authconfiguration

urlpatterns = [
    path('accounts/login/', login, name='login'),
    path('accounts/logout/', auth_views.logout, name='logout'),
    path('accounts/sign-up/', SignUpView.as_view(), name='sign-up'),
    path('users/profile/<int:pk>', profile, name='profile'),
    path('users/whoinnovates/', who_innovates, name='whoinnovates'),
    path('configuration/set/', set_authconfiguration, name='set-configuration'),
    path('configuration/set/', set_authconfiguration, name='edit-configuration'),
]
