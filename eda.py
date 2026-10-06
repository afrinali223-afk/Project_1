import pandas as pd

print("=" * 40)
print("GLOBAL SEISMIC TRENDS - EDA")
print("=" * 40)

# Load cleaned dataset
df = pd.read_csv("data/cleaned_seismic_data.csv")

print("\nDataset shape:")
print(df.shape)

print("\nNumerical summary:")
print(df[['latitude', 'longitude', 'depth_km', 'mag', 'sig']].describe())

print("\nMagnitude category counts:")
print(df['magnitude_category'].value_counts())

print("\nEarthquakes by year:")
print(df['year'].value_counts().sort_index())

import matplotlib.pyplot as plt

print("\nCreating yearly earthquake count chart...")

yearly_counts = df['year'].value_counts().sort_index()

plt.figure(figsize=(10, 6))

plt.bar(
    yearly_counts.index,
    yearly_counts.values
)

plt.title("Number of Earthquakes by Year")
plt.xlabel("Year")
plt.ylabel("Number of Earthquakes")

plt.xticks(yearly_counts.index)

plt.tight_layout()
plt.show()

print("=" * 40)
print("DATE RANGE CHECK")
print("=" * 40)

print("\nEarliest earthquake:")
print(df['time'].min())

print("\nLatest earthquake:")
print(df['time'].max())

print("\nNumber of records by year:")
print(df['year'].value_counts().sort_index())

print("=" * 40)
print("DATE RANGE CHECK")
print("=" * 40)

print("\nEarliest earthquake:")
print(df['time'].min())

print("\nLatest earthquake:")
print(df['time'].max())

print("\nNumber of records by year:")
print(df['year'].value_counts().sort_index())

print("=" * 40)
print("MONTHLY EARTHQUAKE TREND")
print("=" * 40)

monthly_counts = df['month'].value_counts().sort_index()

print("\nEarthquakes by month:")
print(monthly_counts)

plt.figure(figsize=(10, 6))

plt.bar(
    monthly_counts.index,
    monthly_counts.values
)

plt.title("Number of Earthquakes by Month")
plt.xlabel("Month")
plt.ylabel("Number of Earthquakes")

plt.xticks(range(1, 13))

plt.tight_layout()
plt.show()

print("=" * 40)
print("MAGNITUDE DISTRIBUTION")
print("=" * 40)

print("\nMagnitude statistics:")
print(df['mag'].describe())

plt.figure(figsize=(10, 6))

plt.hist(
    df['mag'],
    bins=30
)

plt.title("Distribution of Earthquake Magnitudes")
plt.xlabel("Magnitude")
plt.ylabel("Number of Earthquakes")

plt.tight_layout()
plt.show()

print("=" * 40)
print("MAGNITUDE CATEGORY DISTRIBUTION")
print("=" * 40)

category_counts = (
    df['magnitude_category']
    .value_counts()
    .reindex(['Minor', 'Light', 'Moderate', 'Strong', 'Major'])
)

print("\nEarthquakes by magnitude category:")
print(category_counts)

plt.figure(figsize=(10, 6))

plt.bar(
    category_counts.index,
    category_counts.values
)

plt.title("Earthquakes by Magnitude Category")
plt.xlabel("Magnitude Category")
plt.ylabel("Number of Earthquakes")

plt.tight_layout()
plt.show()

print("=" * 40)
print("EARTHQUAKE DEPTH DISTRIBUTION")
print("=" * 40)

print("\nDepth statistics:")
print(df['depth_km'].describe())

plt.figure(figsize=(10, 6))

plt.hist(
    df['depth_km'],
    bins=30
)

plt.title("Distribution of Earthquake Depths")
plt.xlabel("Depth (km)")
plt.ylabel("Number of Earthquakes")

plt.tight_layout()
plt.show()

print("=" * 40)
print("MAGNITUDE VS DEPTH")
print("=" * 40)

print("\nCorrelation between magnitude and depth:")

correlation = df['mag'].corr(df['depth_km'])

print("Correlation coefficient:", correlation)

plt.figure(figsize=(10, 6))

plt.scatter(
    df['depth_km'],
    df['mag'],
    alpha=0.3,
    s=10
)

plt.title("Earthquake Magnitude vs Depth")
plt.xlabel("Depth (km)")
plt.ylabel("Magnitude")

plt.tight_layout()
plt.show()

print("=" * 40)
print("EARTHQUAKES BY MAGNITUDE CATEGORY")
print("=" * 40)

category_counts = df['magnitude_category'].value_counts()

print(category_counts)

plt.figure(figsize=(10, 6))

category_counts.plot(kind='bar')

plt.title("Earthquakes by Magnitude Category")
plt.xlabel("Magnitude Category")
plt.ylabel("Number of Earthquakes")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

print("=" * 40)
print("EARTHQUAKES BY HOUR")
print("=" * 40)

hour_counts = df['hour'].value_counts().sort_index()

print(hour_counts)

plt.figure(figsize=(10, 6))

hour_counts.plot(kind='bar')

plt.title("Earthquakes by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Earthquakes")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

print("=" * 40)
print("TSUNAMI FLAG DISTRIBUTION")
print("=" * 40)

tsunami_counts = df['tsunami'].value_counts().sort_index()

print(tsunami_counts)

plt.figure(figsize=(8, 6))

tsunami_counts.plot(kind='bar')

plt.title("Earthquakes by Tsunami Flag")
plt.xlabel("Tsunami Flag")
plt.ylabel("Number of Earthquakes")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

print("=" * 40)
print("CHECKING DAY OF WEEK")
print("=" * 40)

print(df[['time', 'day_of_week']].head())

print("\nDay of week counts:")
print(df['day_of_week'].value_counts())

print("=" * 40)
print("DATA QUALITY SUMMARY")
print("=" * 40)

print("\nMissing values by column:")
print(df.isnull().sum())

print("\nTotal duplicate rows:")
print(df.duplicated().sum())

print("\nNumber of unique countries:")
print(df['country'].nunique())

print("\nNumber of unique magnitude types:")
print(df['magType'].nunique())

print("\nMagnitude types:")
print(df['magType'].value_counts())

print("\nNumber of unique reporting networks:")
print(df['net'].nunique())

print("\nTop reporting networks:")
print(df['net'].value_counts().head(10))

print("\nNumber of unique earthquake types:")
print(df['type'].nunique())

print("\nEarthquake types:")
print(df['type'].value_counts())

print("\nNumeric ranges:")
print("\nMagnitude:")
print(df['mag'].min(), "to", df['mag'].max())

print("\nDepth (km):")
print(df['depth_km'].min(), "to", df['depth_km'].max())

print("\nLatitude:")
print(df['latitude'].min(), "to", df['latitude'].max())

print("\nLongitude:")
print(df['longitude'].min(), "to", df['longitude'].max())

print("=" * 40)
print("COUNTRY-LEVEL EARTHQUAKE ANALYSIS")
print("=" * 40)

country_counts = df['country'].value_counts().head(10)

print("\nTop 10 countries by earthquake count:")
print(country_counts)

plt.figure(figsize=(10, 6))

country_counts.sort_values().plot(kind='barh')

plt.title("Top 10 Countries by Earthquake Count")
plt.xlabel("Number of Earthquakes")
plt.ylabel("Country")

plt.tight_layout()
plt.show()

print("=" * 40)
print("AVERAGE MAGNITUDE BY COUNTRY")
print("=" * 40)

country_avg_mag = (
    df.groupby('country')['mag']
    .agg(['mean', 'count'])
    .query('count >= 100')
    .sort_values('mean', ascending=False)
    .head(10)
)

print("\nTop 10 countries by average magnitude:")
print(country_avg_mag)

print("=" * 40)
print("REPORTING NETWORK ANALYSIS")
print("=" * 40)

network_counts = df['net'].value_counts()

print("\nEarthquakes reported by network:")
print(network_counts)

plt.figure(figsize=(10, 6))

network_counts.head(10).sort_values().plot(kind='barh')

plt.title("Top 10 Reporting Networks")
plt.xlabel("Number of Earthquakes")
plt.ylabel("Reporting Network")

plt.tight_layout()
plt.show()

print("=" * 40)
print("STRONG/DEStructive EARTHQUAKE ANALYSIS")
print("=" * 40)

strong_counts = df['strong_destructive_flag'].value_counts()

print("\nStrong/Destructive earthquake counts:")
print(strong_counts)

print("\nStrong/Destructive earthquake percentages:")
print(
    (df['strong_destructive_flag'].value_counts(normalize=True) * 100)
    .round(2)
)

print("\nNumber of earthquakes with magnitude >= 6:")
print((df['mag'] >= 6).sum())

plt.figure(figsize=(8, 6))

strong_counts.plot(kind='bar')

plt.title("Strong/Destructive vs Other Earthquakes")
plt.xlabel("Category")
plt.ylabel("Number of Earthquakes")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

print("=" * 40)
print("SHALLOW VS DEEP EARTHQUAKE ANALYSIS")
print("=" * 40)

depth_category_counts = df['depth_category'].value_counts()

print("\nShallow vs Deep earthquake counts:")
print(depth_category_counts)

print("\nShallow vs Deep earthquake percentages:")
print(
    (df['depth_category'].value_counts(normalize=True) * 100)
    .round(2)
)

plt.figure(figsize=(8, 6))

depth_category_counts.plot(kind='bar')

plt.title("Shallow vs Deep Earthquakes")
plt.xlabel("Depth Category")
plt.ylabel("Number of Earthquakes")

plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

print("=" * 40)
print("DAY OF WEEK ANALYSIS")
print("=" * 40)

day_order = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]

day_counts = (
    df['day_of_week']
    .value_counts()
    .reindex(day_order)
)

print("\nEarthquakes by day of week:")
print(day_counts)

plt.figure(figsize=(10, 6))

day_counts.plot(kind='bar')

plt.title("Earthquakes by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Number of Earthquakes")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

print("=" * 40)
print("MAGNITUDE TYPE ANALYSIS")
print("=" * 40)

print("\nEarthquakes by magnitude type:")

magtype_counts = df['magType'].value_counts()

print(magtype_counts)

plt.figure(figsize=(10, 6))

magtype_counts.plot(kind='bar')

plt.title("Earthquakes by Magnitude Type")
plt.xlabel("Magnitude Type")
plt.ylabel("Number of Earthquakes")

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()


print("\nAverage magnitude by magnitude type:")

magtype_avg = (
    df.groupby('magType')['mag']
    .agg(['mean', 'count'])
    .sort_values('mean', ascending=False)
)

print(magtype_avg)


