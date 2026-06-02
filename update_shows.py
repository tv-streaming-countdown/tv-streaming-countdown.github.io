import os
import json
import requests
import datetime

API_KEY = os.getenv("AI_API_KEY")

# US Eastern Time (EST) setup for absolute automation
est_timezone = datetime.timezone(datetime.timedelta(hours=-4))
us_current_time = datetime.datetime.now(est_timezone)
today_date_us = us_current_time.strftime("%B %d, %Y")

# Strict US Multi-Platform System Instruction for Google Discover & Accuracy
system_instruction = (
    "Act as a professional US Entertainment Journalist and SEO Expert. "
    "Your core mission is to output factual, real-time data for Hollywood movies and TV shows. "
    "STRICT POLICY:\n"
    "1. VERIFICATION: Only use officially confirmed release dates from trusted US entertainment outlets (IMDb, Variety, Deadline, or official platform press releases).\n"
    "2. NO HALLUCINATION: If an exact release date is unconfirmed or TBA, do not make up a date.\n"
    "3. IMAGES FOR DISCOVER: You must provide high-quality, valid, public image URLs for show posters. Ensure they are clean, high-resolution, and optimized for Google Discover cards.\n"
    "4. NO MARKDOWN: Output ONLY raw, valid JSON. Never wrap the output in ```json or any conversational text. Breakage of JSON syntax will crash the platform."
)

# Strict US Multi-Platform Trending + Upcoming Countdown Prompt
prompt = (
    f"Today's date in the United States is {today_date_us}. Based on this live date, "
    "generate a highly accurate entertainment dataset tailored for the US audience containing two specific sections.\n\n"
    "Section 1: upcoming_countdowns (Exactly 3 highly anticipated Hollywood movies or TV series releasing in the US between June 2026 and July 2026. Must be a mix of both theaters and streaming networks. Strict rule: Do NOT include 'The Boys Season 5' or anything released before today).\n\n"
    "Section 2: now_trending (Identify what US audiences are watching most right now. Provide exactly 4 entries in total—exactly 1 top trending movie or TV show currently dominating the viewership charts for EACH of these 4 major US platforms: Netflix US, HBO Max, Hulu, and Prime Video US. Ensure the titles reflect real time search volume and high buzz in the USA).\n\n"
    "The output must be pure clean JSON that strictly matches this structure without any markdown ticks:\n"
    "{\n"
    "  \"upcoming_countdowns\": [\n"
    "    {\n"
    "      \"title\": \"Movie/Show Name\",\n"
    "      \"platform\": \"Theaters / Netflix US / HBO Max / Hulu\",\n"
    "      \"release_date_text\": \"Month DD, 2026\",\n"
    "      \"countdown_date\": \"Month DD, 2026 00:00:00 EDT\",\n"
    "      \"poster_url\": \"Provide a high-quality, valid, public image/poster URL for this show. Strictly output raw text URL, do not add markdown brackets like [] or ()\",\n"
    "      \"description\": \"A catchy 2-sentence description loaded with high-volume US search keywords for Google Discover.\"\n"
    "    }\n"
    "  ],\n"
    "  \"now_trending\": [\n"
    "    {\n"
    "      \"platform\": \"Netflix US\",\n"
    "      \"title\": \"Trending Title on Netflix\",\n"
    "      \"rank\": \"#1 on Platform\",\n"
    "      \"trending_reason\": \"Detailed explanation of why US audiences are binge-watching this right now, using trending buzzwords.\"\n"
    "    },\n"
    "    {\n"
    "      \"platform\": \"HBO Max\",\n"
    "      \"title\": \"Trending Title on HBO Max\",\n"
    "      \"rank\": \"#1 on Platform\",\n"
    "      \"trending_reason\": \"Detailed explanation of why this show is dominating US social media trends and streaming charts today.\"\n"
    "    },\n"
    "    {\n"
    "      \"platform\": \"Hulu\",\n"
    "      \"title\": \"Trending Title on Hulu\",\n"
    "      \"rank\": \"#1 on Platform\",\n"
    "      \"trending_reason\": \"Why this particular content is racking up millions of streaming hours across the United States this week.\"\n"
    "    },\n"
    "    {\n"
    "      \"platform\": \"Prime Video US\",\n"
    "      \"title\": \"Trending Title on Prime Video\",\n"
    "      \"rank\": \"#1 on Platform\",\n"
    "      \"trending_reason\": \"The main factors driving massive viewership and overnight success for this title among US cord-cutters.\"\n"
    "    }\n"
    "  ],\n"
    "  \"seo_title\": \"Top Trending Shows on Netflix, HBO Max, Hulu, Prime Video and Upcoming US Countdowns\",\n"
    "  \"seo_text\": \"Stay track of what is currently trending across major US streaming platforms like Netflix, Hulu, Prime Video, and HBO Max alongside real-time countdown timers for highly anticipated summer 2026 Hollywood movie and TV releases.\"\n"
    "}"
)

url = f"[https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=](https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=){API_KEY}"
headers = {'Content-Type': 'application/json'}

payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "systemInstruction": {"parts": [{"text": system_instruction}]},
    "generationConfig": {
        "responseMimeType": "application/json"
    }
}

# Clean Backup Data without markdown links
backup_data = {
  "upcoming_countdowns": [
    {
      "title": "Toy Story 5",
      "platform": "Theaters",
      "release_date_text": "June 19, 2026",
      "countdown_date": "June 19, 2026 00:00:00 EDT",
      "poster_url": "[https://images.unsplash.com/photo-1608889174639-414d9fde9bf0?w=500&auto=format&fit=crop&q=60](https://images.unsplash.com/photo-1608889174639-414d9fde9bf0?w=500&auto=format&fit=crop&q=60)",
      "description": "The toys are back in theaters! Track the official US release date countdown for Disney Pixar's next blockbuster installment."
    },
    {
      "title": "House of the Dragon Season 3",
      "platform": "HBO Max",
      "release_date_text": "June 21, 2026",
      "countdown_date": "June 21, 2026 21:00:00 EDT",
      "poster_url": "[https://images.unsplash.com/photo-1618336753974-aae8e04506aa?w=500&auto=format&fit=crop&q=60](https://images.unsplash.com/photo-1618336753974-aae8e04506aa?w=500&auto=format&fit=crop&q=60)",
      "description": "Track the live Eastern Standard Time countdown to the highly anticipated premiere of the Targaryen civil war on HBO."
    },
    {
      "title": "The Bear Season 4",
      "platform": "Hulu",
      "release_date_text": "June 25, 2026",
      "countdown_date": "June 25, 2026 00:01:00 EDT",
      "poster_url": "[https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=500&auto=format&fit=crop&q=60](https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=500&auto=format&fit=crop&q=60)",
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
  "seo_title": "US Streaming Charts: Top Trending Shows and Upcoming Movie Countdowns",
  "seo_text": "Track what Americans are watching most right now across Netflix, HBO Max, Hulu, and Prime Video alongside real-time live countdown clocks for the biggest summer 2026 blockbusters."
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
    print("Successfully updated via Gemini US Multi-Platform Engine!")

except Exception as e:
    print(f"API Error, saving multi-platform backup data: {e}")
    with open('shows.json', 'w') as f:
        json.dump(backup_data, f, indent=2)
