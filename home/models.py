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
    p_name = models.CharField(max_length=100)
    p_email = models.EmailField()
    p_phone = models.CharField(max_length=20)
    doc_name = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.p_name} with Dr. {self.doc_name.doc_name} on {self.booking_date} at {self.booked_on}"
