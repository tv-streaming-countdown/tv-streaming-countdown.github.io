import os
import json
import requests

API_KEY = os.getenv("AI_API_KEY")

prompt = (
    "Identify 3 highly anticipated upcoming Hollywood movies or TV series releasing in the US between June and July 2026. "
    "Provide accurate US release dates. "
    "You must return ONLY a valid JSON object. Do not wrap it in markdown code blocks like ```json. "
    "The format must exactly match this structure:\n"
    "{\n"
    "  \"shows\": [\n"
    "    {\n"
    "      \"title\": \"Show Name\",\n"
    "      \"platform\": \"Netflix US / HBO Max / Hulu\",\n"
    "      \"release_date_text\": \"Month DD, 2026\",\n"
    "      \"countdown_date\": \"Month DD, 2026 00:00:00 EDT\",\n"
    "      \"description\": \"A catchy 2-sentence US-focused description with high-volume keywords.\"\n"
    "    }\n"
    "  ],\n"
    "  \"seo_title\": \"An SEO-optimized title for US audience\",\n"
    "  \"seo_text\": \"A detailed 150-word paragraph optimized for Google Discover targeting US entertainment search trends.\"\n"
    "}"
)

url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=){API_KEY}"
headers = {'Content-Type': 'application/json'}
payload = {"contents": [{"parts": [{"text": prompt}]}]}

try:
    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    
    ai_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
    
    if ai_text.startswith("
```"):
        ai_text = ai_text.split("```")[1]
        if ai_text.startswith("json"):
            ai_text = ai_text[4:]
            
    cleaned_json = json.loads(ai_text.strip())
    
    with open('shows.json', 'w') as f:
        json.dump(cleaned_json, f, indent=2)
        
    print("Successfully updated shows.json via Gemini API!")

except Exception as e:
    print(f"Error: {e}")
    exit(1)
