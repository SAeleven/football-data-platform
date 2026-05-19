import json
import os
import pandas as pd


# -----------------------
# LOAD RAW DATA
# -----------------------
def load_latest_file():
    folder = "data/raw"

    files = [f for f in os.listdir(folder) if f.endswith(".json")]

    if not files:
        raise FileNotFoundError("No JSON files found in data/raw")

    latest_file = sorted(files)[-1]
    path = os.path.join(folder, latest_file)

    print(f"Loading file: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# -----------------------
# TRANSFORM
# -----------------------
def extract_matches(data):
    matches = []

    for m in data.get("matches", []):
        matches.append({
            "match_id": m.get("id"),
            "utc_date": m.get("utcDate"),
            "status": m.get("status"),
            "home_team": m.get("homeTeam", {}).get("name"),
            "away_team": m.get("awayTeam", {}).get("name"),
            "home_score": m.get("score", {}).get("fullTime", {}).get("home"),
            "away_score": m.get("score", {}).get("fullTime", {}).get("away"),
            "competition": m.get("competition", {}).get("name")
        })

    return matches


def to_dataframe(matches):
    df = pd.DataFrame(matches)

    if df.empty:
        print("Warning: No matches found")
        return df

    # Convert datetime
    df["utc_date"] = pd.to_datetime(df["utc_date"], errors="coerce")

    return df


# -----------------------
# CLEANING
# -----------------------
def clean_data(df):
    if df.empty:
        return df

    # Remove duplicates
    df = df.drop_duplicates(subset=["match_id"])

    # Handle missing scores (not played yet)
    df["home_score"] = df["home_score"].fillna(-1).astype(int)
    df["away_score"] = df["away_score"].fillna(-1).astype(int)

    # Add useful derived columns
    df["goal_diff"] = df["home_score"] - df["away_score"]

    df["season"] = df["utc_date"].dt.year

    return df


# -----------------------
# SAVE
# -----------------------
def save_parquet(df):
    os.makedirs("data/processed", exist_ok=True)

    output_path = "data/processed/matches.parquet"

    df.to_parquet(output_path, index=False)

    return output_path


# -----------------------
# PIPELINE
# -----------------------
def main():
    print("Starting transformation pipeline...")

    data = load_latest_file()

    matches = extract_matches(data)

    df = to_dataframe(matches)

    df = clean_data(df)

    output_path = save_parquet(df)

    print(f"Done ✅ Saved to: {output_path}")

    print(f"Rows: {len(df)}")
    print(df.head())


if __name__ == "__main__":
    main()