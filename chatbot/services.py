import time

from google import genai
from django.conf import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def generate_chat_response(user_message):

    prompt = f"""
You are the AI Patient Assistant for NovaCare Hospital.

Your role is to help patients with:

- Hospital departments
- Doctors
- Appointment guidance
- General hospital information
- Basic symptom-based department guidance

Important safety rules:

- Do not diagnose diseases.
- Do not prescribe medicines.
- Do not provide medicine dosage.
- Do not replace a doctor.
- If the patient describes a possible emergency,
  advise them to seek immediate medical attention.

Patient message:

{user_message}

Give a simple, friendly and helpful response.
"""

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            print(f"Gemini Error (Attempt {attempt + 1}):", e)

            if attempt < 2:
                time.sleep(2)

            else:
                return (
                    "Sorry, the AI assistant is temporarily busy. "
                    "Please try again in a moment."
                )