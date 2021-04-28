from django.urls import path
from . import views

urlpatterns = [
    path('donor-registration/', views.RegisterDonor.as_view(), name='donor_registration'),
    path('', views.FindDonor, name='find_donor'),
    path('donor/<slug:pk>', views.donor_detail, name='donor_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
]