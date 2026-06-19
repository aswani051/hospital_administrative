from django.contrib import admin
from .models import Department, Doctor, booking

admin.site.register(Department)
admin.site.register(Doctor)
class bookingAdmin(admin.ModelAdmin):
    list_display = ('p_name', 'p_email', 'p_phone', 'doc_name', 'booking_date')
admin.site.register(booking, bookingAdmin)