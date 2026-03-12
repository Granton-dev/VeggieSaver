import json
import base64
from groq import Groq
from django.conf import settings


def analyze_vegetable_photo(image_path):
    client = Groq(
        api_key=settings.GROQ_API_KEY,
        timeout=30.0,  # 30 second timeout
    )

    with open(image_path, 'rb') as f:
        image_data = base64.b64encode(f.read()).decode('utf-8')

    ext = str(image_path).lower().split('.')[-1]
    media_types = {
        'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
        'png': 'image/png', 'webp': 'image/webp'
    }
    media_type = media_types.get(ext, 'image/jpeg')

    # Short focused prompt for faster response
    prompt = """Analyze this vegetable image. Return JSON only, no markdown:
{
  "identified_vegetable": "vegetable name",
  "confidence_score": 0.95,
  "freshness_status": "fresh",
  "freshness_score": 85,
  "condition": "healthy",
  "days_remaining": 5,
  "full_analysis": "brief analysis",
  "recommendations": "what to do now",
  "meal_suggestions": "2 meal ideas",
  "storage_tips": "how to store",
  "warning_signs": [],
  "nutritional_impact": "brief note",
  "household_tip": "one tip"
}
freshness_status: fresh/good/caution/spoiling/spoiled
condition: healthy/wilting/mouldy/bruised/discoloured/pest_damage/disease/unknown"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{media_type};base64,{image_data}"
                    }
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }],
        max_tokens=600,
        temperature=0.1,
    )

    raw_text = response.choices[0].message.content.strip()

    if '```' in raw_text:
        parts = raw_text.split('```')
        for part in parts:
            part = part.strip()
            if part.startswith('json'):
                part = part[4:].strip()
            if part.startswith('{'):
                raw_text = part
                break

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "identified_vegetable": "Unknown",
            "confidence_score": 0.0,
            "freshness_status": "unknown",
            "freshness_score": 0,
            "condition": "unknown",
            "days_remaining": None,
            "full_analysis": raw_text,
            "recommendations": "Please try scanning again with a clearer image.",
            "meal_suggestions": "",
            "storage_tips": "",
            "warning_signs": [],
            "nutritional_impact": "",
            "household_tip": ""
        }


def get_smart_tips(vegetable_names, user=None):
    client = Groq(
        api_key=settings.GROQ_API_KEY,
        timeout=15.0,
    )
    veg_list = ', '.join(vegetable_names) if vegetable_names else 'general vegetables'

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": (
                f"Vegetables I have: {veg_list}. "
                "Give 3 household food waste reduction tips. "
                "JSON array only, no markdown: "
                '[{"title":"...","tip":"...","category":"storage|meal_planning|freshness|shopping"}]'
            )
        }],
        max_tokens=300,
        temperature=0.1,
    )

    try:
        text = response.choices[0].message.content.strip()
        if '```' in text:
            parts = text.split('```')
            for part in parts:
                part = part.strip()
                if part.startswith('json'):
                    part = part[4:].strip()
                if part.startswith('['):
                    text = part
                    break
        return json.loads(text)
    except Exception:
        return [{
            "title": "First In, First Out",
            "tip": "Move older vegetables to the front of your fridge so you use them first.",
            "category": "storage"
        }]