import os
import json
import requests
import datetime

API_KEY = os.getenv("AI_API_KEY")

# US Time Setup
est_timezone = datetime.timezone(datetime.timedelta(hours=-4))
us_current_time = datetime.datetime.now(est_timezone)
today_date_us = us_current_time.strftime("%B %d, %Y")

system_instruction = (
    "Act as a professional US Entertainment Journalist. "
    "STRICT POLICY:\n"
    "1. UNIQUE IMAGES: You MUST provide a different, high-quality, valid public poster URL for EACH show. Do not repeat images.\n"
    "2. NO MARKDOWN: Output ONLY raw JSON. No brackets [] or () around URLs. No backticks.\n"
    "3. DISCOVER READY: Use high-resolution images that look good on Google Discover."
)

prompt = (
    f"Today is {today_date_us}. Generate a US Entertainment dataset in JSON.\n\n"
    "1. upcoming_countdowns: Exactly 3 DIFFERENT Hollywood movies/series releasing in June-July 2026. "
    "For each, provide a UNIQUE poster_url. Do not use the same link twice.\n"
    "2. now_trending: Exactly 4 entries (1 for Netflix, 1 for Max, 1 for Hulu, 1 for Prime Video).\n\n"
    "Structure:\n"
    "{\n"
    "  \"upcoming_countdowns\": [\n"
    "    { \"title\": \"\", \"platform\": \"\", \"release_date_text\": \"\", \"countdown_date\": \"\", \"poster_url\": \"UNIQUE_URL_HERE\", \"description\": \"\" }\n"
    "  ],\n"
    "  \"now_trending\": [\n"
    "    { \"platform\": \"\", \"title\": \"\", \"rank\": \"\", \"trending_reason\": \"\" }\n"
    "  ],\n"
    "  \"seo_title\": \"\", \"seo_text\": \"\"\n"
    "}"
)

# Clean Backup Data with 3 DIFFERENT Images
backup_data = {
  "upcoming_countdowns": [
    {
      "title": "Toy Story 5",
      "platform": "Theaters",
      "release_date_text": "June 19, 2026",
      "countdown_date": "June 19, 2026 00:00:00 EDT",
      "poster_url": "https://images.unsplash.com/photo-1608889174639-414d9fde9bf0?w=500",
      "description": "Buzz and Woody return for a massive summer 2026 release."
    },
    {
      "title": "Supergirl: Woman of Tomorrow",
      "platform": "Theaters",
      "release_date_text": "June 26, 2026",
      "countdown_date": "June 26, 2026 00:00:00 EDT",
      "poster_url": "https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?w=500",
      "description": "The DC Universe expands with a high-stakes cosmic adventure."
    },
    {
      "title": "Moana 2 Live-Action",
      "platform": "Disney+",
      "release_date_text": "July 10, 2026",
      "countdown_date": "July 10, 2026 00:00:00 EDT",
      "poster_url": "https://images.unsplash.com/photo-1559445383-a4d313125553?w=500",
      "description": "A stunning reimagining of the ocean voyager's journey."
    }
  ],
  "now_trending": [
    { "platform": "Netflix US", "title": "Stranger Things 5", "rank": "#1", "trending_reason": "Teasers are breaking the internet." },
    { "platform": "HBO Max", "title": "The Last of Us 2", "rank": "#1", "trending_reason": "Massive viewership for the new season." },
    { "platform": "Hulu", "title": "The Bear Season 4", "rank": "#1", "trending_reason": "High-intensity kitchen drama returns." },
    { "platform": "Prime Video", "title": "Fallout Season 2", "rank": "#1", "trending_reason": "Streaming charts dominance continues." }
  ],
  "seo_title": "Top Trending Shows & Upcoming Countdowns",
  "seo_text": "Real-time updates on what's trending in the USA."
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
    cleaned_json = json.loads(ai_text)
    with open('shows.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_json, f, indent=2, ensure_ascii=False)
    print("Success: 3 Unique Posters Generated!")
except Exception as e:
    print(f"Error: Using Unique Backup Data. {e}")
    with open('shows.json', 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
