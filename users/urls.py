from django.urls import path

from .views import\
    RegisterUserView, LoginView, LogoutView,\
    PasswordChangeView, ProfileView, UpdateProfileView,\
    FriendshipHandlerView, accept_friendship, deny_friendship, \
    remove_friend

app_name = 'users'
urlpatterns = [
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_profile', UpdateProfileView.as_view(), name='update_profile'),

    path('friends', FriendshipHandlerView.as_view(), name='friends'),
    path('friend_accept/<int:pk>', accept_friendship, name='accept_friendship'),
    path('friend_deny/<int:pk>', deny_friendship, name='deny_friendship'),
    path('friend_remove/<int:pk>', remove_friend, name='remove_friend'),

    path('register', RegisterUserView.as_view(), name='register'),

    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('password_change', PasswordChangeView.as_view(), name='password_change')
]
