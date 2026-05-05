import requests
import pandas as pd
import time
from datetime import datetime, timedelta

API_KEY = "AIzaSyDaPGjrn-Se0OXw4jjI8VeFIT1J55_gwJU"

def get_flights(date):

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_flights",
        "departure_id": "EWR",
        "arrival_id": "CUN",
        "outbound_date": date,
        "type": "2", # one-way flights
        "currency": "USD",
        "hl": "en",
        "api_key": API_KEY
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    flights = []

    for section in ["best_flights", "other_flights"]:
        for item in data.get(section, []):
            # airline = ", ".join(f.get("airline", "") for f in item.get("flights", []))
            flights.append({
                "date": date,
                "price": item.get("price"),
                # "airline": airline,
                "stops": max(len(item.get("flights", [])) - 1, 0)
            })
    return flights

# Daily dates: June 1, 2026 to July 31, 2026

start_date = datetime(2026, 6, 1)
end_date = datetime(2026, 7, 31)
dates = []
current = start_date

while current <= end_date:
    dates.append(current.strftime("%Y-%m-%d"))
    current += timedelta(days=1)

print("Total dates to search:", len(dates))

all_data = []

for d in dates:
    try:
        results = get_flights(d)
        all_data.extend(results)
        print(f"Done: {d} | Rows added: {len(results)}")
        time.sleep(1)
    except Exception as e:
        print(f"Error on {d}: {e}")

df = pd.DataFrame(all_data)

# Cleaning up the data with dropna and dropping duplicates

if not df.empty:
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    df = df.drop_duplicates()

# Save file

df.to_csv("flights_data.csv", index=False)
print("\nFinished.")
print("Total rows collected:", len(df))

print(df.head())