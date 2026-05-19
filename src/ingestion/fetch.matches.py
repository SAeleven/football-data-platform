import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# -----------------------
# CONFIG
# -----------------------
load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")

BASE_URL = "https://api.football-data.org/v4"
COMPETITION = "PL"  # Premier League

HEADERS = {
    "X-Auth-Token": API_KEY
}


# -----------------------
# FUNCTIONS
# -----------------------
def fetch_matches():
    """Fetch matches from football-data API"""
    
    url = f"{BASE_URL}/competitions/{COMPETITION}/matches"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(
            f"API Error {response.status_code}: {response.text}"
        )

    return response.json()


def save_raw_data(data):
    """Save raw JSON data locally"""

    os.makedirs("data/raw", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_path = f"data/raw/matches_{COMPETITION}_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return file_path


# -----------------------
# MAIN
# -----------------------
def main():
    print("Fetching matches...")

    data = fetch_matches()

    print("Saving raw data...")

    file_path = save_raw_data(data)

    print(f"Done ✅ File saved at: {file_path}")


if __name__ == "__main__":
    main()