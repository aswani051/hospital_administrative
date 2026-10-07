from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import bookingform, PrescriptionForm
from .models import Department, Doctor, Prescription, booking as Booking
from prescription.models import Prescription
from prescription.gemini_service import patient_assistant



def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def booking(request):

    if request.method == 'POST':

        form = bookingform(request.POST)

        if form.is_valid():

            patient = form.save()

            request.session['token_no'] = patient.token_no

            return redirect('patient_dashboard')

    else:

        form = bookingform()

    return render(
        request,
        'booking.html',
        {
            'form': form
        }
    )


def doctors(request):

    dict_doc = {
        'doctors': Doctor.objects.all()
    }

    return render(
        request,
        'doctors.html',
        dict_doc
    )


def contact(request):

    return render(
        request,
        'contact.html'
    )


def department(request):

    depts = Department.objects.all()

    return render(
        request,
        'department.html',
        {
            'depts': depts
        }
    )


@login_required
def patient_dashboard(request):

    prescriptions = Prescription.objects.all()

    token_no = request.session.get('token_no')
    patient_booking = Booking.objects.filter(
            p_email=request.user.email
        ).select_related(
            'doc_name',
            'doc_name__dep_name'
        ).order_by(
            '-booking_date',
            '-booked_on'
        ).first()

    if request.method == 'POST':

        form = PrescriptionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                'patient_dashboard'
            )

    else:

        form = PrescriptionForm()

    context = {

        'form': form,

        'prescriptions': prescriptions,

        'token_no': token_no,

        'patient_booking': patient_booking

    }

    return render(
        request,
        'patient_dashboard.html',
        context
    )


def patient_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect(
                'patient_dashboard'
            )

    return render(
        request,
        'login.html'
    )
def doctor_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            doctor = Doctor.objects.filter(
                user=user
            ).first()

            if doctor:

                login(request, user)

                return redirect(
                    'doctor_dashboard'
                )

    return render(
        request,
        'doctor_login.html'
    )

@login_required
def profile(request):

    return render(
        request,
        'profile.html'
    )
def ai_patient_assistant(request):

    response = None
    symptoms = ""

    if request.method == 'POST':

        symptoms = request.POST.get(
            'symptoms',
            ''
        ).strip()

        if symptoms:

            try:

                response = patient_assistant(
                    symptoms
                )

            except Exception as e:

                response = f"AI Error: {str(e)}"

    return render(
        request,
        'ai_patient_assistant.html',
        {
            'response': response,
            'symptoms': symptoms,
        }
    )
@login_required
def doctor_dashboard(request):

    doctor = Doctor.objects.filter(
        user=request.user
    ).first()

    if doctor is None:
        return render(
            request,
            'doctor_dashboard.html',
            {
                'doctor': None,
                'appointments': []
            }
        )

    appointments = Booking.objects.filter(
        doc_name=doctor
    ).order_by(
        'booking_date',
        'booked_on'
    )

    return render(
        request,
        'doctor_dashboard.html',
        {
            'doctor': doctor,
            'appointments': appointments
        }
    )