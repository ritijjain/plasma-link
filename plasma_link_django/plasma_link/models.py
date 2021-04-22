from django.db import models
from mapbox_location_field.models import LocationField
from django.contrib.auth.models import User


sex_choices = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

blood_group_choices = [
    (1, 'A+'),
    (2, 'B+'),
    (3, 'AB+'),
    (4, 'O+'),
    (5, 'A-'),
    (6, 'B-'),
    (7, 'AB-'),
    (8, 'O-'),
]

class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=256, choices=sex_choices)

    age = models.IntegerField()
    blood_group = models.IntegerField(choices=blood_group_choices)

    covid_recovory_date = models.DateTimeField()
    
    location = LocationField()

    phone = models.CharField(max_length=256)

    hits = models.IntegerField(default=0)

# regex=r'^\+?1?\d{9,15}$', error_message = ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
