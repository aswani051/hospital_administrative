from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import PrescriptionForm, MedicineFormSet
from .models import Prescription, PrescriptionMedicine

from home.models import Doctor, booking


@login_required
def create_prescription(request, appointment_id):

    appointment = get_object_or_404(
        booking,
        id=appointment_id
    )

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    if request.method == 'POST':

        prescription_form = PrescriptionForm(
            request.POST
        )

        medicine_formset = MedicineFormSet(
            request.POST,
            queryset=PrescriptionMedicine.objects.none()
        )

        if (
            prescription_form.is_valid()
            and medicine_formset.is_valid()
        ):

            # Save prescription
            prescription = prescription_form.save(
                commit=False
            )

            # Connect prescription to patient appointment
            prescription.patient = appointment

            prescription.patient_name = appointment.p_name

            prescription.save()


            # Save medicines
            medicines = medicine_formset.save(
                commit=False
            )

            for medicine in medicines:

                # Skip completely empty medicine rows
                if not medicine.medicine_name:
                    continue

                medicine.prescription = prescription

                medicine.save()


            # Go back to doctor dashboard
            return redirect(
                'doctor_dashboard'
            )

    else:

        prescription_form = PrescriptionForm()

        medicine_formset = MedicineFormSet(
            queryset=PrescriptionMedicine.objects.none()
        )


    return render(
        request,
        'create_prescription.html',
        {
            'prescription_form': prescription_form,

            'medicine_formset': medicine_formset,

            'appointment': appointment,

            'doctor': doctor,
        }
    )


@login_required
def view_prescription(request, prescription_id):

    prescription = get_object_or_404(
        Prescription,
        id=prescription_id
    )

    doctor = get_object_or_404(
        Doctor,
        user=request.user
    )

    return render(
        request,
        'view_prescription.html',
        {
            'prescription': prescription,

            'appointment': prescription.patient,

            'doctor': doctor,
        }
    )