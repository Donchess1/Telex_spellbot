from django.http import JsonResponse
from rest_framework.decorators import api_view
import json

@api_view(['GET'])
def get_markdown_json(request):
    try:
        with open("spellbot/integrationspec.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return JsonResponse(data)
    except FileNotFoundError:
        return JsonResponse({"error": "Markdown JSON file not found"}, status=404)