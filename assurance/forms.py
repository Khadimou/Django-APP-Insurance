from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class InscriptionForm(UserCreationForm):
    telephone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'telephone']

from assurance.models import Vehicle, Info

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['VEHICLE_TYPE', 'VEHICLE_YEAR', 'AGE', 'DRIVING_EXPERIENCE', 'SPEEDING_VIOLATIONS', 'DUIS', 'VEHICLE_OWNERSHIP', 'PAST_ACCIDENTS']

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ['CIVILITY','FIRST_NAME','LAST_NAME','EMAIL', 'DRIVING_EXPERIENCE', 'CAR_OWNERSHIP', 'CLAIMS']