# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, user_login, user_logout,delete_profile

app_name = 'accountsHSM'

urlpatterns = [
    path('register/', register, name='register'),
    path('', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('delete_profile/', delete_profile, name='delete_profile'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]