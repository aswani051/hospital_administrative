from django.urls import path
from . import views


urlpatterns = [

    path(
        'create/<int:appointment_id>/',
        views.create_prescription,
        name='create_prescription'
    ),
path('view/<int:prescription_id>/', views.view_prescription, name='view_prescription'),
]