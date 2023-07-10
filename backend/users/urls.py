from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import path


app_name = 'users'

urlpatterns = [
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(template_name=('users'
                                  '/password_reset_form.html')
                                  ),
        name='password_reset'
    ),
]