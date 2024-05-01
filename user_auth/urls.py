from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import user_login, register, modify_account, admin_management, user_logout
urlpatterns = [
    path("logout/", user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('admin-management/', admin_management, name='admin_management'),
    path('modify-account/<int:user_id>/', modify_account, name='modify_account'),
]