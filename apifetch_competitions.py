import requests
import json

API_KEY = "ckc7OdyL3JPERtBFrwatfZM0o61ogQtAiZA7WR7A"
BASE_URL = "https://api.sportradar.com/tennis/production/v3"

# USE A REAL CATEGORY ID FROM STEP 2
category_urn = "sr:category:6"   # Example: ATP

url = f"{BASE_URL}/en/categories/{category_urn}/competitions.json"

params = {
    "api_key": API_KEY
}

try:
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    print(json.dumps(data, indent=2))

except requests.exceptions.HTTPError as e:
    print("HTTP Error:", e)
    print("response:", response.text)

except Exception as e:
    print("Error:", e)



