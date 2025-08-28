# forms.py
from django import forms
from .models import Patient, Visit, Referrals, CHPProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'date_of_birth', 'gender', 'phone_number', 'village']



class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['symptoms', 'notes']


class ReferralForm(forms.ModelForm):
    class Meta:
        model = Referrals
        fields = ['patient_name', 'age', 'gender', 'symptoms', 'referral_type', 'facility']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}))
    phone = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Phone Number'}))
    region = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Region'}))
    facility_assigned = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Facility Assigned'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email', 'phone', 'region', 'facility_assigned', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        # Create CHPProfile linked to this user
        CHPProfile.objects.create(
            user=user,
            phone=self.cleaned_data['phone'],
            region=self.cleaned_data['region'],
            facility_assigned=self.cleaned_data['facility_assigned']
        )
        return user