import pandas as pd
import re
print("========================================")
print("LOADING RAW DATA")
print("========================================")

df = pd.read_csv("data/earthquakes_raw.csv")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nFirst 5 rows:")
print(df.head())

print("\n========================================")
print("CONVERTING TIMESTAMPS")
print("========================================")

df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
df["updated"] = pd.to_datetime(df["updated"], utc=True, errors="coerce")

print(df[["time", "updated"]].head())

df["time"] = pd.to_datetime(df["time"], utc=True, errors="coerce")
df["updated"] = pd.to_datetime(df["updated"], utc=True, errors="coerce")

print("\n========================================")
print("CLEANING TEXT COLUMNS")
print("========================================")

text_columns = [
    "magType",
    "status",
    "type",
    "net",
    "sources",
    "types"
]

for column in text_columns:
    df[column] = df[column].fillna("unknown")
    df[column] = df[column].astype(str).str.strip()
    df[column] = df[column].str.lower()

print("Text columns cleaned successfully.")

print("\n========================================")
print("CLEANING PLACE COLUMN")
print("========================================")

df["place"] = df["place"].fillna("unknown")
df["place"] = df["place"].astype(str).str.strip()

print("Place column cleaned successfully.")

print("\n========================================")
print("EXTRACTING COUNTRY")
print("========================================")

def extract_country(place):
    match = re.search(r",\s*([^,]+)$", place)

    if match:
        return match.group(1).strip()

    return "unknown"


df["country"] = df["place"].apply(extract_country)
df["country"] = df["country"].str.lower()

print("Country extraction completed.")

print("\nSample country values:")
print(df[["place", "country"]].head(10))

print("\n========================================")
print("CONVERTING NUMERIC COLUMNS")
print("========================================")

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

print("Numeric columns converted successfully.")

print("\nNumeric data types:")
print(df[numeric_columns].dtypes)

print("\n========================================")
print("MISSING VALUE ANALYSIS")
print("========================================")

missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]

print(missing_values)

print("\n========================================")
print("HANDLING MISSING VALUES")
print("========================================")

# Fill missing numeric values with median
numeric_missing_columns = [
    "nst",
    "dmin",
    "rms",
    "gap"
]

for column in numeric_missing_columns:
    median_value = df[column].median()
    df[column] = df[column].fillna(median_value)

print("Missing numeric values handled using median.")

# Check remaining missing values in important columns
remaining_missing = df[
    ["time", "updated", "nst", "dmin", "rms", "gap"]
].isnull().sum()

print("\nRemaining missing values:")
print(remaining_missing)

print("=" * 40)
print("CONVERTING DATE/TIME COLUMNS")
print("=" * 40)

df['time'] = pd.to_datetime(df['time'], errors='coerce')
df['updated'] = pd.to_datetime(df['updated'], errors='coerce')

print("Date/time columns converted successfully.")

print("\nMissing values after conversion:")
print(df[['time', 'updated']].isnull().sum())

print("=" * 40)
print("REMOVING ROWS WITH MISSING TIME")
print("=" * 40)

before = len(df)

df = df.dropna(subset=['time'])

after = len(df)

print("Rows before:", before)
print("Rows after:", after)
print("Rows removed:", before - after)

print("=" * 40)
print("CHECKING DUPLICATES")
print("=" * 40)

duplicates = df.duplicated().sum()

print("Duplicate rows:", duplicates)

print("=" * 40)
print("CHECKING IMPORTANT COLUMNS")
print("=" * 40)

important_columns = [
    'time',
    'latitude',
    'longitude',
    'depth_km',
    'mag',
    'magType',
    'place',
    'tsunami',
    'sig'
]

# Check which columns are available in the dataset
available_columns = [
    col for col in important_columns
    if col in df.columns
]

print("Available important columns:")
print(available_columns)

print("\nMissing values in important columns:")
print(df[available_columns].isnull().sum())

print("=" * 40)
print("CHECKING NUMERICAL RANGES")
print("=" * 40)

print("\nLatitude range:")
print(df['latitude'].min(), "to", df['latitude'].max())

print("\nLongitude range:")
print(df['longitude'].min(), "to", df['longitude'].max())

print("\nDepth range:")
print(df['depth_km'].min(), "to", df['depth_km'].max())

print("\nMagnitude range:")
print(df['mag'].min(), "to", df['mag'].max())

print("\nSignificance (sig) range:")
print(df['sig'].min(), "to", df['sig'].max())

print("=" * 40)
print("CHECKING DUPLICATES")
print("=" * 40)

duplicates = df.duplicated().sum()

print("Duplicate rows:", duplicates)

print("=" * 40)
print("CREATING TIME FEATURES")
print("=" * 40)


df['year'] = df['time'].dt.year
df['month'] = df['time'].dt.month
df['day'] = df['time'].dt.day
df['hour'] = df['time'].dt.hour
df['date'] = df['time'].dt.date
df['day_of_week'] = df['time'].dt.day_name()

df['depth_category'] = df['depth_km'].apply(
    lambda x: 'Shallow' if x < 50 else 'Deep'
)

df['strong_destructive_flag'] = df['mag'].apply(
    lambda x: 'Strong/Destructive' if x >= 6 else 'Not Strong'
)

print("Time features created successfully.")

print("\nSample time features:")
print(df[['time', 'year', 'month', 'day', 'hour', 'date']].head())

print("=" * 40)
print("FINAL MISSING VALUE CHECK")
print("=" * 40)

missing_values = df.isnull().sum()

print(missing_values[missing_values > 0])

print("=" * 40)
print("CREATING MAGNITUDE CATEGORIES")
print("=" * 40)

def magnitude_category(mag):
    if mag < 3:
        return 'Minor'
    elif mag < 5:
        return 'Light'
    elif mag < 6:
        return 'Moderate'
    elif mag < 7:
        return 'Strong'
    else:
        return 'Major'

df['magnitude_category'] = df['mag'].apply(magnitude_category)

print("Magnitude categories created successfully.")

print("\nMagnitude category counts:")
print(df['magnitude_category'].value_counts())

print("=" * 40)
print("FINAL CLEANED DATASET CHECK")
print("=" * 40)

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum()[df.isnull().sum() > 0])

print("\nFirst 5 rows:")
print(df.head())

print("=" * 40)
print("SAVING CLEANED DATASET")
print("=" * 40)

print("\nColumns before saving:")
print(df.columns.tolist())

output_path = "data/cleaned_seismic_data.csv"

df.to_csv(output_path, index=False)

print("Cleaned dataset saved successfully.")
print("File:", output_path)
print("Rows:", len(df))
print("Columns:", len(df.columns))



