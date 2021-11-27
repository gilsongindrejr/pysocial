from django.urls import path

from dashboard.views import DashboardView, delete_post

app_name = 'dashboard'
urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('dashboard/delete_post/<int:pk>', delete_post, name='delete_post'),
]
