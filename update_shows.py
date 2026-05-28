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

backup_data = {
  "shows": [
    {
      "title": "House of the Dragon Season 3",
      "platform": "HBO Max",
      "release_date_text": "June 21, 2026",
      "countdown_date": "June 21, 2026 21:00:00 EDT",
      "description": "Track the live Eastern Standard Time countdown to the highly anticipated premiere of the Targaryen civil war."
    },
    {
      "title": "The Boys Season 5",
      "platform": "Prime Video",
      "release_date_text": "July 10, 2026",
      "countdown_date": "July 10, 2026 00:01:00 EDT",
      "description": "Live release countdown synchronized with official Amazon Prime drops for United States audiences."
    }
  ],
  "seo_title": "Never Miss US Streaming Premiere Times",
  "seo_text": "Our smart countdown clocks are synced to official network release schedules in EST and PT, offering the most accurate tracking tool for cord-cutters in the United States."
}

try:
    if not API_KEY:
        raise ValueError("API Key is missing!")
        
    response = requests.post(url, headers=headers, json=payload, timeout=15)
    response_data = response.json()
    
    ai_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
    
    # Clean code blocks simply without any if-conditions
    ai_text = ai_text.replace("```json", "").replace("```", "").strip()
            
    cleaned_json = json.loads(ai_text)
    
    with open('shows.json', 'w') as f:
        json.dump(cleaned_json, f, indent=2)
    print("Successfully updated via Gemini API!")

except Exception as e:
    print(f"API Error, using backup data: {e}")
    with open('shows.json', 'w') as f:
        json.dump(backup_data, f, indent=2)
