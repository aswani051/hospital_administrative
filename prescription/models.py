from django.db import models
from django.utils import timezone
from home.models import booking


class Prescription(models.Model):

    # Old fields - kept for existing records
    image = models.ImageField(
        upload_to='prescriptions/',
        blank=True,
        null=True
    )

    extracted_text = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

    medicine = models.CharField(
        max_length=200,
        blank=True
    )

    dosage = models.CharField(
        max_length=200,
        blank=True
    )

    patient_name = models.CharField(
        max_length=100,
        blank=True
    )

    # Patient appointment
    patient = models.ForeignKey(
        booking,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        blank=True,
        null=True
    )

    # New prescription information
    symptoms = models.TextField(
        blank=True
    )

    diagnosis = models.TextField(
        blank=True
    )

    additional_instructions = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def __str__(self):

        if self.patient:
            return f"Prescription - {self.patient.p_name}"

        if self.patient_name:
            return f"Prescription - {self.patient_name}"

        return f"Prescription #{self.id}"


class PrescriptionMedicine(models.Model):

    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='medicines'
    )

    medicine_name = models.CharField(
        max_length=200
    )

    dosage = models.CharField(
        max_length=100
    )

    frequency = models.CharField(
        max_length=100
    )

    duration = models.CharField(
        max_length=100
    )

    instructions = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return self.medicine_name