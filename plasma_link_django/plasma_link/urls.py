from django.urls import path
from . import views

urlpatterns = [
    path('donor', views.RegisterDonor.as_view(), name='register_donor'),
]