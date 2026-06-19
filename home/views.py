from django.shortcuts import render
from django.http import HttpResponse

from .forms import bookingform
from .models import Department, Doctor


# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def booking(request):
    if request.method == 'POST':
        form = bookingform(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'conformatin.html')
    form = bookingform()
    return render(request, 'booking.html', {'form': form})


def doctors(request):
    dict_doc = {
        'doctors': Doctor.objects.all()
    }
    return render(request, 'doctors.html', dict_doc)


def contact(request):
    return render(request, 'contact.html')


def department(request):
    depts = Department.objects.all()
    return render(request, 'department.html', {'depts': depts})