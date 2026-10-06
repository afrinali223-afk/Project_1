import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Last 5 years
end_date = datetime.now(timezone.utc)
start_date = end_date.replace(year=end_date.year - 5)

all_earthquakes = []

current_start = start_date

while current_start < end_date:

    # Calculate next month
    if current_start.month == 12:
        current_end = current_start.replace(
            year=current_start.year + 1,
            month=1,
            day=1
        )
    else:
        current_end = current_start.replace(
            month=current_start.month + 1,
            day=1
        )

    # Don't go beyond final date
    if current_end > end_date:
        current_end = end_date

    print(
        "Fetching:",
        current_start.strftime("%Y-%m-%d"),
        "to",
        current_end.strftime("%Y-%m-%d")
    )

    params = {
        "format": "geojson",
        "starttime": current_start.strftime("%Y-%m-%d"),
        "endtime": current_end.strftime("%Y-%m-%d"),
        "minmagnitude": 2.5,
        "limit": 20000,
        "orderby": "time"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()

        for earthquake in data["features"]:

            properties = earthquake["properties"]
            geometry = earthquake["geometry"]

            all_earthquakes.append({
                "id": earthquake.get("id"),

                "time": properties.get("time"),
                "updated": properties.get("updated"),

                "latitude": geometry["coordinates"][1],
                "longitude": geometry["coordinates"][0],
                "depth_km": geometry["coordinates"][2],

                "mag": properties.get("mag"),
                "magType": properties.get("magType"),
                "place": properties.get("place"),

                "status": properties.get("status"),
                "tsunami": properties.get("tsunami"),
                "sig": properties.get("sig"),

                "net": properties.get("net"),
                "nst": properties.get("nst"),
                "dmin": properties.get("dmin"),
                "rms": properties.get("rms"),
                "gap": properties.get("gap"),

                "magError": properties.get("magError"),
                "depthError": properties.get("depthError"),
                "magNst": properties.get("magNst"),

                "locationSource": properties.get("locationSource"),
                "magSource": properties.get("magSource"),

                "types": properties.get("types"),
                "ids": properties.get("ids"),
                "sources": properties.get("sources"),

                "type": properties.get("type")
            })

        print("Records collected:", len(data["features"]))

    else:
        print("API Error:", response.status_code)

    current_start = current_end


# Convert to DataFrame
df = pd.DataFrame(all_earthquakes)

# Remove duplicate earthquake IDs
df = df.drop_duplicates(subset="id")

print("\n========================================")
print("DATA COLLECTION COMPLETED")
print("========================================")

print("Total records:", len(df))
print("Number of columns:", len(df.columns))

print("\nFirst 5 rows:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)
print("\n========================================")
print("MISSING VALUE ANALYSIS")
print("========================================")

missing_values = df.isnull().sum()

print(missing_values)
print("\n========================================")
print("DUPLICATE CHECK")
print("========================================")

print("Duplicate IDs:", df["id"].duplicated().sum())
print("\n========================================")
print("CONVERTING TIMESTAMPS")
print("========================================")

df["time"] = pd.to_datetime(df["time"], unit="ms", utc=True)
df["updated"] = pd.to_datetime(df["updated"], unit="ms", utc=True)

print(df[["time", "updated"]].head())
print("\nData types:")
print(df[["time", "updated"]].dtypes)
numeric_columns = [
    "latitude",
    "longitude",
    "depth_km",
    "mag",
    "tsunami",
    "sig",
    "nst",
    "dmin",
    "rms",
    "gap",
    "magError",
    "depthError",
    "magNst"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

print("\nNumeric columns converted successfully.")

print(df[numeric_columns].dtypes)
print("\n========================================")
print("CHECKING USGS API PROPERTIES")
print("========================================")

test_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

test_params = {
    "format": "geojson",
    "starttime": "2021-09-30",
    "endtime": "2021-10-01",
    "minmagnitude": 2.5,
    "limit": 1
}

test_response = requests.get(test_url, params=test_params)

test_data = test_response.json()

properties = test_data["features"][0]["properties"]

print("\nUSGS property names:")
print(properties.keys())

print("\nUSGS property values:")
for key, value in properties.items():
    print(key, "=", value)
    
print("\n========================================")
print("SAVING RAW DATA")
print("========================================")

df.to_csv("data/earthquakes_raw.csv", index=False)

print("Raw data saved successfully.")