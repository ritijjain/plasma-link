from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name ='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name ='logout'),
    path('delete-account/', user_views.delete_account, name='delete_account')
]
