from django import forms
from .models import MedicalData

class MedicalDataForm(forms.ModelForm):
    class Meta:
        model = MedicalData
        fields = ['patient_id', 'name', 'age', 'diagnosis', 'date']
