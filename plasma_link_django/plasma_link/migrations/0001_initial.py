# Generated by Django 3.2 on 2021-04-18 21:52

from django.db import migrations, models
import mapbox_location_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=256)),
                ('age', models.IntegerField()),
                ('blood_group', models.IntegerField(choices=[(1, 'A+'), (2, 'B+'), (3, 'AB+'), (4, 'O+'), (5, 'A-'), (6, 'B-'), (7, 'AB-'), (8, 'O-')])),
                ('covid_recovory_date', models.DateTimeField()),
                ('location', mapbox_location_field.models.LocationField(map_attrs={})),
                ('phone', models.CharField(max_length=256)),
            ],
        ),
    ]
