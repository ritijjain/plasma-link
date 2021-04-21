from django.urls import path
from . import views

urlpatterns = [
    path('register_donor', views.DonorCreateView.as_view(), name='register_donor'),
]