from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .services import generate_chat_response


def chatbot_page(request):
    return render(request, "chatbot/chatbot.html")


@require_POST
def chat_api(request):

    try:
        data = json.loads(request.body)

        message = data.get("message", "").strip()

        if not message:
            return JsonResponse({
                "success": False,
                "error": "Message cannot be empty."
            }, status=400)

        response = generate_chat_response(message)

        return JsonResponse({
            "success": True,
            "response": response
        })

    except Exception as e:

        print("Chatbot Error:", e)

        return JsonResponse({
            "success": False,
            "error": "Something went wrong."
        }, status=500)