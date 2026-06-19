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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)