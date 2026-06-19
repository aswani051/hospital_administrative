from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_prescription, name='upload'),
    path('history/', views.history, name='history'),
    path(
        'update-status/<int:prescription_id>/<str:new_status>/',
        views.update_status,
        name='update_status'
    ),
    path('delete/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),
    path('dashboard/', views.dashboard, name='dashboard'),

]