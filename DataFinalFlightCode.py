import requests
import pandas as pd
import time
from datetime import datetime, timedelta

API_KEY = "3c07f6fa1f82f96954e83288529d98df111be7f2e397bc2f6ad6203474d646e7"
def get_flights(date):

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_flights",
        "departure_id": "EWR",
        "arrival_id": "CUN",
        "outbound_date": date,
        "type": "2",
        "currency": "USD",
        "hl": "en",
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    flights = []

    for section in ["best_flights", "other_flights"]:
        for item in data.get(section, []):
            flights.append({
                "date": date,
                "price": item.get("price")
            })
    data = response.json()
    print(data)
    return flights


start = datetime(2026, 6, 1)
end = datetime(2026, 7, 31)

dates = []
while start <= end:
    dates.append(start.strftime("%Y-%m-%d"))
    start += timedelta(days=1)

all_data = []
for d in dates:
    results = get_flights(d)
    all_data.extend(results)
    time.sleep(1)
    

df = pd.DataFrame(all_data)
print("columns:", df.columns)
print("rows collected:", len(df))
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df = df.dropna(subset=["price"])
df = df.drop_duplicates()
df.to_csv("flights_data4.csv", index=False)
print(df.head())
