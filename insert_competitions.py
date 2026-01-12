import requests
import mysql.connector

# ---------------- CONFIG ----------------
API_KEY = "ckc7OdyL3JPERtBFrwatfZM0o61ogQtAiZA7WR7A"
API_URL = "https://api.sportradar.com/tennis/production/v3/en/competitions.json"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "game_analytics"
}

# ---------------- FETCH DATA ----------------
response = requests.get(API_URL, params={"api_key": API_KEY})
response.raise_for_status()
data = response.json()

competitions = data.get("competitions", [])
print(f"Total competitions fetched: {len(competitions)}")

# ---------------- DATABASE ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

category_query = """
INSERT IGNORE INTO categories (category_id, category_name)
VALUES (%s, %s)
"""

competition_query = """
INSERT IGNORE INTO competitions
(competition_id, competition_name, parent_id, type, gender, level, category_id)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# ---------------- INSERT DATA ----------------
for comp in competitions:
    category = comp.get("category", {})

    cursor.execute(
        category_query,
        (category.get("id"), category.get("name"))
    )

    cursor.execute(
        competition_query,
        (
            comp.get("id"),
            comp.get("name"),
            comp.get("parent_id"),
            comp.get("type"),
            comp.get("gender"),
            comp.get("level"),
            category.get("id")
        )
    )

conn.commit()
cursor.close()
conn.close()

print(" Competitions & Categories inserted successfully!")



