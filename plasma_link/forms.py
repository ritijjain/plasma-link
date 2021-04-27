from django.forms import Form, CharField, ModelForm, HiddenInput, DateInput, IntegerField, BooleanField, ChoiceField
from datetime import date, timedelta
from django import forms
from mapbox_location_field.models import LocationField
from .models import Donor
from django.forms.widgets import DateInput
from bootstrap_datepicker_plus import DatePickerInput
from mapbox_location_field.forms import LocationField
from intl_tel_input.widgets import IntlTelInputWidget
from django.utils import timezone




class RegisterDonorForm(ModelForm):

    class Meta:
        model = Donor
        fields = ['age', 'sex', 'blood_group', 'covid_recovory_date', 'location', 'phone']
        widgets = {
            'covid_recovory_date': DatePickerInput(),
            'phone': IntlTelInputWidget(default_code='in'),
        }    
    weight_pass = BooleanField(label='My bodyweight is at least 50 kg or more.', required=False)
    pregnant_pass = BooleanField(label='I have never been pregnant before.', required=False)
    diabetic_pass = BooleanField(label='I am not a diabetic.', required=False)
    chronic_desease_pass = BooleanField(label='I do not have chronic kidney/heart/lung or liver disease.', required=False)
    cancer_pass = BooleanField(label='I am not a cancer survivor.', required=False)
    surgery_tattoo_pass = BooleanField(label='I have not underwent surgery or had a tattoo in the past six months.', required=False)
    hiv_pass = BooleanField(label='I am not HIV/AIDS positive.', required=False)
    vaccine_pass = BooleanField(label='I have not had a COVID vaccine in the last 14 days.', required=False)


    def clean(self):
        cleaned_data = self.cleaned_data

        age = cleaned_data.get('age')

        covid_recovory_date = cleaned_data.get('covid_recovory_date')

        weight_pass = cleaned_data.get('weight_pass')
        pregnant_pass = cleaned_data.get('pregnant_pass')
        diabetic_pass = cleaned_data.get('diabetic_pass')
        chronic_desease_pass = cleaned_data.get('chronic_desease_pass')
        cancer_pass = cleaned_data.get('cancer_pass')
        surgery_tattoo_pass = cleaned_data.get('surgery_tattoo_pass')
        hiv_pass = cleaned_data.get('hiv_pass')
        vaccine_pass = cleaned_data.get('vaccine_pass')

        # Validate age
        if age < 18 or age > 55:
            raise forms.ValidationError(f'Sorry you are ineligible, you must be between 18 - 55 years old.')
        
        # Validate covid_recovory_date
        covid_recovory_date = cleaned_data.get('covid_recovory_date')
        if timezone.now() - timedelta(days = 14) < covid_recovory_date:
            raise forms.ValidationError(f'Sorry you are ineligible, you must wait at least 14 days after you recover from COVID')

        # Validate eligibility
        if not all([weight_pass, pregnant_pass, diabetic_pass, chronic_desease_pass, cancer_pass, surgery_tattoo_pass, hiv_pass, vaccine_pass]):
            raise forms.ValidationError(f'Sorry you are ineligible, you fail to meet one or more eligibility requirements.')
        
        # Phone check
        phone = cleaned_data.get('phone')
        if not phone.replace('+', '').isdecimal() or len(phone) > 15:
            raise forms.ValidationError(f'Your Phone/Mobile number is invalid. Please provide a valid Phone/Mobile number without any country codes')

    
        return cleaned_data


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

class FindDonorForm(Form):
    search_location = LocationField()
    blood_group = ChoiceField(choices=blood_group_choices, required=False)

class Verify(Form):
    pass

        
