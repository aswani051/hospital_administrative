from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [

 path('', views.index, name='home'),
 path('about/', views.about, name='about'),
 path('booking/', views.booking, name='booking'),
 path('doctors/', views.doctors, name='doctors'),
 path('contact/', views.contact, name='contact'),
 path('department/', views.department, name='department'),
 path('prescription/', include('prescription.urls')),
 path('patient-dashboard/',views.patient_dashboard,name='patient_dashboard'),
 path('login/', views.patient_login, name='login'),
 path('profile/', views.profile, name='profile'),
 path(
    'ai-patient-assistant/',
    views.ai_patient_assistant,
    name='ai_patient_assistant'
),
 path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
 path('doctor-login/', views.doctor_login, name='doctor_login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)