from django.db import models

class Prescription(models.Model):
    image = models.ImageField(upload_to='prescriptions/')
    extracted_text = models.TextField(blank=True)

    patient_name = models.CharField(max_length=100, blank=True)
    medicine = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=200, blank=True)

    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.patient_name or "Prescription"