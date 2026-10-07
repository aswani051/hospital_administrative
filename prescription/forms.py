
from django import forms
from django.forms import modelformset_factory

from .models import Prescription, PrescriptionMedicine


class PrescriptionForm(forms.ModelForm):

    class Meta:
        model = Prescription

        fields = [
            'symptoms',
            'diagnosis',
            'additional_instructions',
        ]

        widgets = {

            'symptoms': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the symptoms reported by the patient...',
                'rows': 4,
            }),

            'diagnosis': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Enter the doctor's diagnosis...",
                'rows': 4,
            }),

            'additional_instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter additional instructions...',
                'rows': 4,
            }),

        }


class PrescriptionMedicineForm(forms.ModelForm):

    class Meta:
        model = PrescriptionMedicine

        fields = [
            'medicine_name',
            'dosage',
            'frequency',
            'duration',
            'instructions',
        ]

        widgets = {

            'medicine_name': forms.TextInput(attrs={
                'class': 'medicine-input',
                'placeholder': 'Medicine name',
            }),

            'dosage': forms.TextInput(attrs={
                'class': 'medicine-input',
                'placeholder': 'Dosage',
            }),

            'frequency': forms.TextInput(attrs={
                'class': 'medicine-input',
                'placeholder': '1-0-1',
            }),

            'duration': forms.TextInput(attrs={
                'class': 'medicine-input',
                'placeholder': '5 days',
            }),

            'instructions': forms.TextInput(attrs={
                'class': 'medicine-input',
                'placeholder': 'After food',
            }),

        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Medicine fields are optional.
        # This allows the extra empty row to stay empty.

        for field in self.fields.values():
            field.required = False


MedicineFormSet = modelformset_factory(
    PrescriptionMedicine,
    form=PrescriptionMedicineForm,
    extra=1,
    can_delete=True
)
