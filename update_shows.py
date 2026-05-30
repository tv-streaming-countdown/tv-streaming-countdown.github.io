import os
import json
import requests
import datetime

API_KEY = os.getenv("AI_API_KEY")

# US Eastern Time (EST) setup
est_timezone = datetime.timezone(datetime.timedelta(hours=-4))
us_current_time = datetime.datetime.now(est_timezone)
today_date_us = us_current_time.strftime("%B %d, %Y")

# Strict Prompt: Mix of Movies and TV Shows strictly enforced
prompt = (
    f"Today's date in the United States is {today_date_us}. Based on this date, "
    "identify exactly 3 highly anticipated upcoming Hollywood releases in the US between June 2026 and July 2026. "
    "Strict Instruction 1: You MUST include a mix of BOTH upcoming Hollywood theatrical movies and major TV series (e.g., 2 movies and 1 show, or 1 movie and 2 shows). Do not just give TV series.\n"
    "Strict Instruction 2: Do NOT include 'The Boys Season 5' or any content already released before today.\n"
    "Strict Instruction 3: Target only US theaters or US streaming (Netflix US, HBO Max, Hulu, Disney+ US, Prime Video US).\n\n"
    "The format must exactly match this JSON structure:\n"
    "{\n"
    "  \"shows\": [\n"
    "    {\n"
    "      \"title\": \"Movie or Show Name\",\n"
    "      \"platform\": \"Theaters / Netflix US / HBO Max / Hulu\",\n"
    "      \"release_date_text\": \"Month DD, 2026\",\n"
    "      \"countdown_date\": \"Month DD, 2026 00:00:00 EDT\",\n"
    "      \"description\": \"A catchy 2-sentence US-focused description with high-volume keywords for Google Discover targeting USA entertainment search trends.\"\n"
    "    }\n"
    "  ],\n"
    "  \"seo_title\": \"An SEO-optimized title for US audience and Google Discover\",\n"
    "  \"seo_text\": \"A detailed 150-word paragraph optimized for Google Discover targeting US entertainment search trends and theater goers.\"\n"
    "}"
)

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "responseMimeType": "application/json"
    }
}

# New Backup Data with exactly 3 items (Including Movies and Shows mixed!)
backup_data = {
  "shows": [
    {
      "title": "Superman (2025/2026 Movie)",
      "platform": "Theaters",
      "release_date_text": "July 11, 2026",
      "countdown_date": "July 11, 2026 00:00:00 EDT",
      "description": "Track the live countdown to the cinematic release of James Gunn's highly anticipated Superman movie in US theaters."
    },
    {
      "title": "House of the Dragon Season 3",
      "platform": "HBO Max",
      "release_date_text": "June 21, 2026",
      "countdown_date": "June 21, 2026 21:00:00 EDT",
      "description": "Track the live Eastern Standard Time countdown to the highly anticipated premiere of the Targaryen civil war on HBO."
    },
    {
      "title": "The Bear Season 4",
      "platform": "Hulu",
      "release_date_text": "June 25, 2026",
      "countdown_date": "June 25, 2026 00:01:00 EDT",
      "description": "Get ready for the intense kitchen drama with our live countdown synchronized for official Hulu US streaming launch times."
    }
  ],
  "seo_title": "Upcoming US Movies and Streaming Premiere Times",
  "seo_text": "Get the most accurate live countdown clocks for highly anticipated Hollywood movies hitting theaters and TV shows premiering on Netflix, Hulu, and HBO Max synced directly to official US release schedules."
}

try:
    if not API_KEY:
        raise ValueError("API Key is missing!")
        
    response = requests.post(url, headers=headers, json=payload, timeout=20)
    response_data = response.json()
    
    ai_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
    cleaned_json = json.loads(ai_text)
    
    with open('shows.json', 'w') as f:
        json.dump(cleaned_json, f, indent=2)
    print("Successfully updated via Gemini 1.5 Flash US Movie Engine!")

except Exception as e:
    print(f"API Error, using US backup data: {e}")
    with open('shows.json', 'w') as f:
        json.dump(backup_data, f, indent=2)
