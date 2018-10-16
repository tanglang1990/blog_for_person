from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from users.forms import AuthForm
from . import views

app_name = 'users'
urlpatterns = [
    path('register', views.register, name='register'),
    path('success', views.success, name='success'),

    path('login/', auth_views.LoginView.as_view(
        template_name='users/base_form.html',
        form_class=AuthForm,
        extra_context=dict(title='用户登录')), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='users:login'), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='users/base_form.html',
        success_url=reverse_lazy('users:success'),
        title = '修改密码'
    ), name='password_change'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/base_form.html',
        success_url=reverse_lazy('users:success'),
        email_template_name='users/email.html',
        title = '忘记密码'
    ), name='password_reset'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/base_form.html',
        success_url=reverse_lazy('users:success')
    ), name='password_reset_confirm'),
]
