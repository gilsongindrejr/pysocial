from django.urls import path

from .views import RegisterUserView, LoginView, LogoutView, PasswordChangeView, ProfileView

app_name = 'users'
urlpatterns = [
    path('profile', ProfileView.as_view(), name='profile'),

    path('register', RegisterUserView.as_view(), name='register'),

    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('password_change', PasswordChangeView.as_view(), name='password_change')
]
