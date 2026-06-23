from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Doctor(models.Model):
    doc_name = models.CharField(max_length=100)
    doc_spec = models.CharField(max_length=100)
    dep_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    doc_img = models.ImageField(upload_to='doctors/')

    def __str__(self):
        return self.doc_name


class booking(models.Model):

    token_no = models.PositiveIntegerField(
        unique=True,
        editable=False,
        null=True
    )

    p_name = models.CharField(max_length=100)
    p_email = models.EmailField()
    p_phone = models.CharField(max_length=20)

    doc_name = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE
    )

    booking_date = models.DateField()

    booked_on = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if self.token_no is None:

            last_booking = booking.objects.exclude(
                token_no__isnull=True
            ).order_by('-token_no').first()

            if last_booking:
                self.token_no = last_booking.token_no + 1
            else:
                self.token_no = 1

        super().save(*args, **kwargs)

    def __str__(self):

        return f"Token {self.token_no} - {self.p_name}"
class Prescription(models.Model):
    patient_name = models.CharField(max_length=100)
    prescription_file = models.FileField(upload_to='prescriptions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name