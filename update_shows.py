import os
import json
import requests
import datetime

API_KEY = os.getenv("AI_API_KEY")

# US Time Setup
est_timezone = datetime.timezone(datetime.timedelta(hours=-4))
us_current_time = datetime.datetime.now(est_timezone)
today_date_us = us_current_time.strftime("%B %d, %Y")

# AI ko strictly alag images ke liye instruct karna
system_instruction = (
    "You are a Hollywood Database API. Your output MUST be unique.\n"
    "CRITICAL: Each 'poster_url' MUST have a unique ID at the end. \n"
    "Example 1: https://images.unsplash.com/photo-1?w=800n"
    "Example 2: https://images.unsplash.com/photo-2?w=800n"
    "Example 3: https://images.unsplash.com/photo-3?w=800n"
    "NEVER repeat the same URL twice in one JSON response."
)

prompt = (
    f"Today: {today_date_us}. Provide JSON for 3 upcoming Hollywood shows (June-July 2026).\n"
    "Ensure 'poster_url' for each show is a DIFFERENT high-quality image link from Unsplash with unique IDs."
)

# Har baar alag dikhne wala Backup Data (Just in case)
backup_data = {
  "upcoming_countdowns": [
    {
      "title": "Toy Story 5",
      "poster_url": "https://images.unsplash.com/photo-1608889174639-414d9fde9bf0?w=800",
      "release_date_text": "June 19, 2026",
      "countdown_date": "June 19, 2026 00:00:00 EDT"
    },
    {
      "title": "Supergirl",
      "poster_url": "https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?w=800",
      "release_date_text": "June 26, 2026",
      "countdown_date": "June 26, 2026 00:00:00 EDT"
    },
    {
      "title": "Moana 2",
      "poster_url": "https://images.unsplash.com/photo-1559445383-a4d313125553?w=800",
      "release_date_text": "July 10, 2026",
      "countdown_date": "July 10, 2026 00:00:00 EDT"
    }
  ]
}

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "systemInstruction": {"parts": [{"text": system_instruction}]},
    "generationConfig": {"responseMimeType": "application/json"}
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=20)
    ai_text = response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    data = json.loads(ai_text)
    
    # --- IMAGE FIXING LOGIC ---
    # Agar AI ne same image de di, toh hum manually ID badal denge
    seen_urls = []
    for i, show in enumerate(data.get('upcoming_countdowns', [])):
        current_url = show.get('poster_url', '')
        if current_url in seen_urls or not current_url:
            # Naya unique ID force karein
            show['poster_url'] = f"https://images.unsplash.com/photo-{1600000000000 + (i*5000)}?w=800"
        seen_urls.append(show['poster_url'])
    # --------------------------

    with open('shows.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Success: Unique images verified and saved!")

except Exception as e:
    with open('shows.json', 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
    print(f"Used backup due to error: {e}")
