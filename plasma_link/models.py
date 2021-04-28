from django.db import models
from mapbox_location_field.models import LocationField
from django.contrib.auth.models import User
from django.db.models.expressions import RawSQL
from math import cos, asin, sqrt, pi
from location_field.models.plain import PlainLocationField
import secrets


sex_choices = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]

blood_group_choices = [
    ('A+', 'A+'),
    ('B+', 'B+'),
    ('AB+', 'AB+'),
    ('O+', 'O+'),
    ('A-', 'A-'),
    ('B-', 'B-'),
    ('AB-', 'AB-'),
    ('O-', 'O-'),
]

import math
from django.db.backends.signals import connection_created
from django.dispatch import receiver

class Donor(models.Model):
    id = models.CharField(max_length=256, primary_key=True, default=secrets.token_urlsafe)

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    sex = models.CharField(max_length=256, choices=sex_choices)

    age = models.IntegerField(help_text='Donors must be between 18 - 55 year old.')
    blood_group = models.CharField(max_length=256, choices=blood_group_choices)

    covid_recovory_date = models.DateTimeField(help_text='The approximate date when all your COVID symptoms subsided or you tested negative for COVID.')
    
    location = LocationField(
        help_text='Enter the approximate location of your locality. This location is only used for location based search to help locate the closest donors.',
        map_attrs={'track_location_button': True, 'center': [76.9512635, 28.6923329], 'readonly': True, 'zoom': 4})

    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    phone = models.CharField(max_length=256, verbose_name='Phone/Mobile')

    views = models.IntegerField(default=0)
    phone = models.CharField(max_length=256)

    def process_lat_lon(self):
        self.latitude = self.location[0]
        self.longitude = self.location[1]

    
    # Credit: rphlo's answer on https://stackoverflow.com/questions/19703975/django-sort-by-distance
    @classmethod
    def get_locations_nearby_coords(self, latitude, longitude, max_distance=None):
        """
        Return objects sorted by distance to specified coordinates
        which distance is less than max_distance given in kilometers
        """
        # Great circle distance formula
        gcd_formula = "6371 * acos(least(greatest(cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)) \, -1), 1))"
        distance_raw_sql = RawSQL(gcd_formula, (latitude, longitude, latitude))
        qs = self.objects.all().annotate(distance=distance_raw_sql).order_by('distance')
        if max_distance is not None:
            qs = qs.filter(distance__lt=max_distance)
        return qs


    def calc_distance(self, latitude, longitude):
        p = pi/180
        a = 0.5 - cos((float(self.location[0])-latitude)*p)/2 + cos(latitude*p) * cos(float(self.location[0])*p) * (1-cos((float(self.location[1])-longitude)*p))/2
        return 12742 * asin(sqrt(a))