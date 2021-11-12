from django.urls import path

from .views import RegisterUserView, LoginView, LogoutView, PasswordChangeView

urlpatterns = [
    path('register', RegisterUserView.as_view()),

    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),

    path('password_change', PasswordChangeView.as_view())
]
