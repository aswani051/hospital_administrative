from google import genai
from django.conf import settings
import json

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def analyze_prescription(text):

    prompt = f"""
    Read this prescription.

    {text}

    Extract medicines.

    Return ONLY a JSON array.

    Example:

    [
      {{
        "medicine":"Paracetamol",
        "dosage":"650 mg",
        "time":"Night"
      }}
    ]

    Rules:

    - Return only JSON
    - No explanation
    - No markdown
    - No extra text
    - If unavailable write Not Found
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return json.loads(response.text)


def patient_assistant(symptoms):

    prompt = f"""
You are an AI Patient Assistant for a hospital website.

A patient has described the following symptoms:

{symptoms}

Provide safe and simple general health guidance.

Your response should include:

1. Possible general causes or conditions that may be related to the symptoms.
2. Basic self-care guidance when appropriate.
3. The hospital department that may be suitable for consultation.
4. Clear warning signs that require urgent medical attention.

Important rules:

- Do NOT provide a definite diagnosis.
- Do NOT prescribe medicines or give medicine dosages.
- Do NOT replace a doctor.
- If the symptoms may indicate an emergency, clearly advise the patient to seek immediate medical attention.
- Use simple language that a normal patient can understand.
- Keep the response concise and organized.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text