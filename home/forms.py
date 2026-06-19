from django import forms
from .models import booking

class dateinput(forms.DateInput):
    input_type = 'date'

class bookingform(forms.ModelForm):
    class Meta:
        model = booking
        fields = '__all__'

        widgets = {
            'p_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),

            'p_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }),

            'p_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),

            'doc_name': forms.Select(attrs={
                'class': 'form-select'
            }),

            'booking_date': dateinput(attrs={
                'class': 'form-control'
            }),
        }

        labels = {
            'p_name': 'Full Name',
            'p_email': 'Email Address',
            'p_phone': 'Phone Number',
            'doc_name': 'Select Doctor',
            'booking_date': 'Booking Date',
        }