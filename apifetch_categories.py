import requests
import json

# ---------------- CONFIG ----------------
API_KEY = "ckc7OdyL3JPERtBFrwatfZM0o61ogQtAiZA7WR7A"

BASE_URL = "https://api.sportradar.com/tennis/trial/v3"

# Example category (WTA)
CATEGORY_URN = "sr:category:6"   # WTA

# ---------------- API URL ----------------
url = f"{BASE_URL}/en/categories/{CATEGORY_URN}/competitions.json"

params = {
    "api_key": API_KEY
}

headers = {
    "accept": "application/json"
}

# ---------------- REQUEST ----------------
response = requests.get(url, params=params, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
    print(f"\nTotal competitions fetched: {len(data.get('competitions', []))}")
else:
    print("API Error:", response.status_code)
    print(response.text)

