from django.urls import path
from . import views
from .views import register, login_view, profile, reset_password, home
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name = 'home'),
    path('register/', register, name = 'register'),
    # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', login_view, name = 'login'),
    path('profile/', profile, name = 'profile'),
    path('reset-password/', reset_password, name = 'reset-password'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'users/logout.html'), name = 'logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'users/password_reset.html'), name = 'password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'), name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name = 'password_reset_complete'),
    path('', views.profile, name='users-home'),  # Redirect to the 'profile' view
]
