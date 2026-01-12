import requests
import mysql.connector

# ---------------- CONFIG ----------------
API_KEY = "ckc7OdyL3JPERtBFrwatfZM0o61ogQtAiZA7WR7A"

URL = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "game_analytics"
}

# ---------------- API CALL ----------------
response = requests.get(URL, params={"api_key": API_KEY})

if response.status_code != 200:
    print("API request failed:", response.text)
    raise SystemExit

data = response.json()

# ---------------- READ DATA ----------------
rankings = data.get("rankings", [])

if not rankings:
    print("No rankings found in response")
    raise SystemExit

doubles_rankings = rankings[0].get("competitor_rankings", [])

print(f"Total doubles competitors: {len(doubles_rankings)}")

# ---------------- DATABASE INSERT ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

for item in doubles_rankings:
    competitor = item["competitor"]

    # Insert competitor
    cursor.execute("""
        INSERT IGNORE INTO competitors
        (competitor_id, name, country, country_code, abbreviation)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        competitor["id"],
        competitor["name"],
        competitor.get("country", ""),
        competitor.get("country_code", ""),
        competitor.get("abbreviation", "")
    ))

    # Insert ranking
    cursor.execute("""
        INSERT INTO competitor_rankings
        (ranking, movement, points, competitions_played, competitor_id)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        item["rank"],
        item["movement"],
        item["points"],
        item["competitions_played"],
        competitor["id"]
    ))

conn.commit()
cursor.close()
conn.close()

print(" Doubles rankings inserted successfully!")
