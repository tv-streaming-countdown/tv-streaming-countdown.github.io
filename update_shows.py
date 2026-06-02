import os
import json
import requests
import datetime

API_KEY = os.getenv("AI_API_KEY")

# US Eastern Time (EST) setup for absolute automation
est_timezone = datetime.timezone(datetime.timedelta(hours=-4))
us_current_time = datetime.datetime.now(est_timezone)
today_date_us = us_current_time.strftime("%B %d, %Y")

# Strict US Multi-Platform System Instruction for Text-Only Data
system_instruction = (
    "Act as a professional US Entertainment Journalist and SEO Expert.\n"
    "Your core mission is to output factual, real-time data for Hollywood movies and TV shows.\n"
    "STRICT POLICY:\n"
    "1. ALL SECTIONS REQUIRED: You must output both 'upcoming_countdowns' and 'now_trending' sections.\n"
    "2. NO MARKDOWN: Output ONLY raw, valid JSON. Never wrap the output in ```json or any conversational text.\n"
    "3. NO IMAGES NEEDED: Do not worry about image URLs. Keep focus entirely on high-volume US search keywords."
)

# Prompt tailored for the new clean index.html layout
prompt = (
    f"Today's date in the United States is {today_date_us}. Based on this live date, "
    "generate a highly accurate entertainment dataset tailored for the US audience containing two specific sections.\n\n"
    "Section 1: upcoming_countdowns (Exactly 3 highly anticipated Hollywood movies or TV series releasing in the US between June 2026 and July 2026. Must be a mix of both theaters and streaming networks).\n\n"
    "Section 2: now_trending (Provide exactly 4 entries in total—exactly 1 top trending movie or TV show currently dominating the viewership charts for EACH of these 4 major US platforms: Netflix US, HBO Max, Hulu, and Prime Video US).\n\n"
    "The output must be pure clean JSON that strictly matches this structure without any markdown ticks:\n"
    "{\n"
    "  \"upcoming_countdowns\": [\n"
    "    {\n"
    "      \"title\": \"Movie/Show Name\",\n"
    "      \"platform\": \"Theaters / Netflix US / HBO Max / Hulu\",\n"
    "      \"release_date_text\": \"Month DD, 2026\",\n"
    "      \"countdown_date\": \"Month DD, 2026 00:00:00 EDT\",\n"
    "      \"description\": \"A catchy 2-sentence description loaded with high-volume US search keywords for Google Discover.\"\n"
    "    }\n"
    "  ],\n"
    "  \"now_trending\": [\n"
    "    { \"platform\": \"Netflix US\", \"title\": \"Trending Title\", \"rank\": \"#1 on Platform\", \"trending_reason\": \"Explanation\" },\n"
    "    { \"platform\": \"HBO Max\", \"title\": \"Trending Title\", \"rank\": \"#1 on Platform\", \"trending_reason\": \"Explanation\" },\n"
    "    { \"platform\": \"Hulu\", \"title\": \"Trending Title\", \"rank\": \"#1 on Platform\", \"trending_reason\": \"Explanation\" },\n"
    "    { \"platform\": \"Prime Video US\", \"title\": \"Trending Title\", \"rank\": \"#1 on Platform\", \"trending_reason\": \"Explanation\" }\n"
    "  ],\n"
    "  \"seo_title\": \"Upcoming Hollywood Movies 2026 | US Streaming Charts\",\n"
    "  \"seo_text\": \"Stay track of what is currently trending across major US streaming platforms like Netflix, Hulu, Prime Video, and HBO Max alongside real-time countdown timers for highly anticipated summer 2026 Hollywood movie and TV releases.\"\n"
    "}"
)

# Text-Only Fallback / Fail-safe Data
backup_data = {
  "upcoming_countdowns": [
    {
      "title": "Toy Story 5",
      "platform": "Theaters",
      "release_date_text": "June 19, 2026",
      "countdown_date": "June 19, 2026 00:00:00 EDT",
      "description": "The toys are back in theaters! Track the official US release date countdown for Disney Pixar's next blockbuster installment."
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
  "now_trending": [
    {
      "platform": "Netflix US",
      "title": "Stranger Things Season 5 Hype",
      "rank": "#1 on Platform",
      "trending_reason": "Massive streaming spikes and breaking social media trends in the US as official production teasers dominate entertainment feeds."
    },
    {
      "platform": "HBO Max",
      "title": "The Last of Us Season 2",
      "rank": "#1 on Platform",
      "trending_reason": "Viewership records are breaking weekly across the United States as fans tune in for the intense live-action adaptation episodes."
    },
    {
      "platform": "Hulu",
      "title": "Shogun Season 2 Updates",
      "rank": "#1 on Platform",
      "trending_reason": "Binge-watching trends climb overnight as US audiences revisit the award-winning historical drama following major casting news."
    },
    {
      "platform": "Prime Video US",
      "title": "Fallout Season 2 Previews",
      "rank": "#1 on Platform",
      "trending_reason": "Dominating the charts as official streaming discussions and high-volume Google searches surge for Amazon's flagship sci-fi franchise."
    }
  ],
  "seo_title": "Upcoming Hollywood Movies 2026 | US Streaming Charts",
  "seo_text": "Track what Americans are watching most right now across Netflix, HBO Max, Hulu, and Prime Video alongside real-time live countdown clocks for the biggest summer 2026 blockbusters."
}

url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=){API_KEY}"
headers = {'Content-Type': 'application/json'}
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "systemInstruction": {"parts": [{"text": system_instruction}]},
    "generationConfig": {
        "responseMimeType": "application/json"
    }
}

try:
    if not API_KEY:
        raise ValueError("API Key is missing from GitHub Secrets!")
        
    response = requests.post(url, headers=headers, json=payload, timeout=20)
    response_data = response.json()
    
    ai_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
    data = json.loads(ai_text)
    
    # --- HARD PROTECTION LOGIC (No Images Needed) ---
    # 1. Validation for Countdowns
    if 'upcoming_countdowns' not in data or len(data['upcoming_countdowns']) < 3:
        data['upcoming_countdowns'] = backup_data['upcoming_countdowns']

    # 2. Validation for Trending Section (Netflix, Hulu etc.)
    if 'now_trending' not in data or len(data['now_trending']) < 4:
        data['now_trending'] = backup_data['now_trending']
        
    if 'seo_title' not in data:
        data['seo_title'] = backup_data['seo_title']
    if 'seo_text' not in data:
        data['seo_text'] = backup_data['seo_text']

    # Final Write with Encoding Fix
    with open('shows.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Successfully updated via Gemini Engine (Text Optimized)!")

except Exception as e:
    print(f"API/Parsing Error, saving backup data: {e}")
    with open('shows.json', 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False)
