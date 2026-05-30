import os
import json
import requests
import datetime

API_KEY = os.getenv("AI_API_KEY")

# US Eastern Time (EST) nikalne ke liye zone offset setup
# Isse GitHub server par chalte waqt bhi exact US ki date milegi
est_timezone = datetime.timezone(datetime.timedelta(hours=-4)) # EDT (Summer Offset)
us_current_time = datetime.datetime.now(est_timezone)
today_date_us = us_current_time.strftime("%B %d, %Y")

# Strict Prompt for US Audience & US Timezones
prompt = (
    f"Today's date in the United States is {today_date_us}. Based on this current US date, "
    "identify 3 highly anticipated upcoming Hollywood movies or TV series releasing in the US between June 2026 and July 2026. "
    "Strict Instruction 1: Do NOT include 'The Boys Season 5' or any show that has already premiered or ended in the US before today.\n"
    "Strict Instruction 2: Only include shows available on US streaming platforms (e.g., Netflix US, HBO Max, Hulu, Prime Video, Disney+ US) or US theaters.\n"
    "Strict Instruction 3: Ensure 'countdown_date' matches the exact US premiere time, typically formatted in EDT/EST.\n\n"
    "The format must exactly match this JSON structure:\n"
    "{\n"
    "  \"shows\": [\n"
    "    {\n"
    "      \"title\": \"Show Name\",\n"
    "      \"platform\": \"Netflix US / HBO Max / Hulu / Prime Video\",\n"
    "      \"release_date_text\": \"Month DD, 2026\",\n"
    "      \"countdown_date\": \"Month DD, 2026 00:00:00 EDT\",\n"
    "      \"description\": \"A catchy 2-sentence US-focused description with high-volume keywords for Google Discover targeting USA entertainment search trends.\"\n"
    "    }\n"
    "  ],\n"
    "  \"seo_title\": \"An SEO-optimized title for US audience and Google Discover\",\n"
    "  \"seo_text\": \"A detailed 150-word paragraph optimized for Google Discover targeting US entertainment search trends and cord-cutters.\"\n"
    "}"
)

# Latest Gemini 1.5 Flash API URL
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
headers = {'Content-Type': 'application/json'}

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "responseMimeType": "application/json"
    }
}

# Bullet-proof Backup Data tailored for US Market
backup_data = {
  "shows": [
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
  "seo_title": "Never Miss US Streaming Premiere Times",
  "seo_text": "Our smart countdown clocks are synced to official network release schedules in EST and PT, offering the most accurate tracking tool for entertainment lovers in the United States."
}

try:
    if not API_KEY:
        raise ValueError("API Key is missing from GitHub Secrets!")
        
    response = requests.post(url, headers=headers, json=payload, timeout=20)
    response_data = response.json()
    
    ai_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
    cleaned_json = json.loads(ai_text)
    
    with open('shows.json', 'w') as f:
        json.dump(cleaned_json, f, indent=2)
    print("Successfully updated via Gemini 1.5 Flash US Engine!")

except Exception as e:
    print(f"API Error, using US backup data: {e}")
    with open('shows.json', 'w') as f:
        json.dump(backup_data, f, indent=2)
