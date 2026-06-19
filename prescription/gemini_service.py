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