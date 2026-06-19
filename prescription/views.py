from django.shortcuts import render, redirect
from .forms import PrescriptionForm
from .models import Prescription

import easyocr
from rapidfuzz import process
import os

from .gemini_service import analyze_prescription

# -------------------------
# EasyOCR Reader
# -------------------------

reader = easyocr.Reader(['en'])

# -------------------------
# Medicines File
# -------------------------

MEDICINES_FILE = os.path.join(
    os.path.dirname(__file__),
    'medicines.txt'
)

with open(
    MEDICINES_FILE,
    'r',
    encoding='utf-8'
) as file:

    MEDICINE_LIST = [

        line.strip()

        for line in file

        if line.strip()

    ]


# -------------------------
# Upload Prescription
# -------------------------

def upload_prescription(request):

    if request.method == 'POST':

        form = PrescriptionForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            obj = form.save()

            # OCR

            results = reader.readtext(
                obj.image.path
            )

            text = ""

            for result in results:

                text += result[1] + "\n"

            patient = "Not Detected"

            medicine = "Not Detected"

            dosage = "Not Detected"

            lines = [

                line.strip()

                for line in text.split('\n')

                if line.strip()

            ]

            # -------------------------
            # Patient Detection
            # -------------------------

            for i, line in enumerate(lines):

                if "name" in line.lower():

                    patient_parts = []

                    for j in range(
                        i + 1,
                        min(i + 4, len(lines))
                    ):

                        next_line = lines[j]

                        if (

                            "date" in next_line.lower()

                            or "age" in next_line.lower()

                            or "address" in next_line.lower()

                        ):

                            break

                        patient_parts.append(
                            next_line
                        )

                    patient = " ".join(
                        patient_parts
                    ).strip()

                    if patient:

                        break

            # -------------------------
            # Dosage Detection
            # -------------------------

            dosages = []

            for line in lines:

                if (

                    "mg" in line.lower()

                    or "tablet" in line.lower()

                    or "capsule" in line.lower()

                    or "daily" in line.lower()

                ):

                    dosages.append(line)

            if dosages:

                dosage = ", ".join(

                    list(
                        dict.fromkeys(
                            dosages
                        )
                    )[:3]

                )

            # -------------------------
            # Medicine Detection
            # -------------------------

            detected_medicines = []

            for line in lines:

                match = process.extractOne(

                    line,

                    MEDICINE_LIST,

                    score_cutoff=80

                )

                if match:

                    medicine_name = match[0]

                    if medicine_name not in detected_medicines:

                        detected_medicines.append(
                            medicine_name
                        )

            if detected_medicines:

                medicine = ", ".join(
                    detected_medicines
                )

            # -------------------------
            # Gemini AI Table
            # -------------------------

            try:

                medicine_table = analyze_prescription(
                    text
                )

            except Exception:

                medicine_table = []

            # -------------------------
            # Save Database
            # -------------------------

            obj.extracted_text = text

            obj.patient_name = patient

            obj.medicine = medicine

            obj.dosage = dosage

            obj.save()

            return render(

                request,

                'result.html',

                {

                    'text': text,

                    'patient': patient,

                    'medicine': medicine,

                    'dosage': dosage,

                    'detected_medicines': detected_medicines,

                    'medicine_table': medicine_table,

                }

            )

    else:

        form = PrescriptionForm()

    return render(

        request,

        'upload.html',

        {

            'form': form

        }

    )


# -------------------------
# History
# -------------------------

def history(request):

    search = request.GET.get(
        'search'
    )

    prescriptions = (

        Prescription.objects

        .all()

        .order_by('-id')

    )

    if search:

        prescriptions = prescriptions.filter(

            patient_name__icontains=search

        )

    return render(

        request,

        'history.html',

        {

            'prescriptions': prescriptions,

            'search': search,

        }

    )


# -------------------------
# Update Status
# -------------------------

def update_status(

    request,

    prescription_id,

    new_status

):

    prescription = Prescription.objects.get(

        id=prescription_id

    )

    prescription.status = new_status

    prescription.save()

    return redirect('history')


# -------------------------
# Delete
# -------------------------

def delete_prescription(

    request,

    prescription_id

):

    prescription = Prescription.objects.get(

        id=prescription_id

    )

    prescription.delete()

    return redirect('history')


# -------------------------
# Dashboard
# -------------------------

def dashboard(request):

    total = Prescription.objects.count()

    pending = Prescription.objects.filter(

        status='Pending'

    ).count()

    processing = Prescription.objects.filter(

        status='Processing'

    ).count()

    ready = Prescription.objects.filter(

        status='Ready'

    ).count()

    dispensed = Prescription.objects.filter(

        status='Dispensed'

    ).count()

    return render(

        request,

        'dashboard.html',

        {

            'total': total,

            'pending': pending,

            'processing': processing,

            'ready': ready,

            'dispensed': dispensed,

        }

    )