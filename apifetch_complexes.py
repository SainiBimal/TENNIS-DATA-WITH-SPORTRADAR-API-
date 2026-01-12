import requests
import mysql.connector

# ---------------- CONFIG ----------------
API_KEY = "ckc7OdyL3JPERtBFrwatfZM0o61ogQtAiZA7WR7A"
API_URL = "https://api.sportradar.com/tennis/production/v3/en/complexes.json"

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

complexes = data.get("complexes", [])
print(f"Total complexes fetched: {len(complexes)}")

# ---------------- DB CONNECTION ----------------
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# ---------------- INSERT DATA ----------------
for complex_item in complexes:
    complex_id = complex_item["id"]
    complex_name = complex_item["name"]

    # Insert Complex
    cursor.execute("""
        INSERT IGNORE INTO complexes (complex_id, complex_name)
        VALUES (%s, %s)
    """, (complex_id, complex_name))

    # Insert Venues
    for venue in complex_item.get("venues", []):
        cursor.execute("""
            INSERT IGNORE INTO venues
            (venue_id, venue_name, city_name, country_name,
             country_code, timezone, complex_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            venue["id"],
            venue["name"],
            venue.get("city", {}).get("name"),
            venue.get("country", {}).get("name"),
            venue.get("country", {}).get("code"),
            venue.get("timezone"),
            complex_id
        ))

conn.commit()
cursor.close()
conn.close()

print(" Complexes & Venues inserted successfully!")

