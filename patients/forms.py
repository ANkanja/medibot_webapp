# forms.py
from django import forms
from .models import Patient, Visit

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'date_of_birth', 'gender', 'phone_number', 'village']



class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['symptoms', 'notes']






