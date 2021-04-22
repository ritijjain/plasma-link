from django.forms import Form, CharField, ModelForm, HiddenInput, DateInput, IntegerField, BooleanField, ChoiceField
from datetime import date
from django import forms
from mapbox_location_field.models import LocationField
from .models import Donor
from django.forms.widgets import DateInput
from bootstrap_datepicker_plus import DatePickerInput
from mapbox_location_field.forms import LocationField



class RegisterDonorForm(ModelForm):

    weight_fail = BooleanField(label='Do weight less than 50 kg?', required=False)
    pregnant_fail = BooleanField(label='Have you ever been pregnant?', required=False)
    diabetic_fail = BooleanField(label='Are you a diabetic?', required=False)
    chronic_desease_fail = BooleanField(label='Do you have chronic kidney/heart/lung or liver disease?', required=False)
    cancer_fail = BooleanField(label='Are you a cancer survivor?', required=False)
    surgery_tattoo_fail = BooleanField(label='Have you underwent surgery or had a tattoo in the past six months?', required=False)
    hiv_fail = BooleanField(label='Are you HIV/AIDS positive?', required=False)

    class Meta:
        model = Donor
        fields = ['age', 'sex', 'blood_group', 'covid_recovory_date', 'location']
        widgets = {
            'covid_recovory_date': DatePickerInput(),
        }


    def clean(self):
        cleaned_data = super().clean()

        age = cleaned_data.get('age')

        covid_recovory_date = cleaned_data.get('covid_recovory_date')

        weight_fail = cleaned_data.get('weight_fail')
        pregnant_fail = cleaned_data.get('pregnant_fail')
        diabetic_fail = cleaned_data.get('diabetic_fail')
        chronic_desease_fail = cleaned_data.get('chronic_desease_fail')
        cancer_fail = cleaned_data.get('cancer_fail')
        surgery_tattoo_fail = cleaned_data.get('surgery_tattoo_fail')
        hiv_fail = cleaned_data.get('hiv_fail')

        # Validate age
        if age < 18 or age > 55:
            raise forms.ValidationError(f'Sorry you are ineligible, you must be between 18 - 55 years old.')
        
        # Validate covid_recovory_date
        covid_recovory_date = cleaned_data.get('covid_recovory_date')
        # if covid_recovory_date

        # Validate eligibility
        if any([weight_fail, pregnant_fail, diabetic_fail, chronic_desease_fail, cancer_fail, surgery_tattoo_fail, hiv_fail]):
            raise forms.ValidationError(f'Sorry you are ineligible because you fail to meet the illegibility criteria.')

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

class FindDonorForm(ModelForm):
    location = LocationField()
    blood_group = ChoiceField(choices=blood_group_choices, required=False)

        
