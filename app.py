import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Global Seismic Trends",
    page_icon="🌍",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

file_path = "data/cleaned_seismic_data.csv"

df = pd.read_csv(file_path)

df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Make sure numeric columns are numeric
numeric_columns = [
    "year",
    "month",
    "day",
    "hour",
    "latitude",
    "longitude",
    "depth_km",
    "mag",
    "tsunami",
    "nst",
    "rms",
    "gap"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")


# ============================================================
# TITLE
# ============================================================

st.title("🌍 Global Seismic Trends Dashboard")

st.write(
    "Interactive analysis of global seismic activity "
    "based on USGS earthquake data from the last five years."
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Dashboard Filters")

years = sorted(df["year"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "📅 Select Year",
    options=years,
    default=years
)


magnitude_categories = sorted(
    df["magnitude_category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "📊 Magnitude Category",
    options=magnitude_categories,
    default=magnitude_categories
)


event_types = sorted(
    df["type"].dropna().unique()
)

selected_types = st.sidebar.multiselect(
    "🌋 Event Type",
    options=event_types,
    default=event_types
)


tsunami_options = sorted(
    df["tsunami"].dropna().unique()
)

selected_tsunami = st.sidebar.multiselect(
    "🌊 Tsunami",
    options=tsunami_options,
    default=tsunami_options
)


# Country filter
if "country" in df.columns:

    countries = sorted(
        df["country"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_countries = st.sidebar.multiselect(
        "🌍 Country",
        options=countries,
        default=[]
    )

else:
    selected_countries = []


# Magnitude range
min_mag = float(df["mag"].min())
max_mag = float(df["mag"].max())

selected_mag_range = st.sidebar.slider(
    "📈 Magnitude Range",
    min_value=min_mag,
    max_value=max_mag,
    value=(min_mag, max_mag)
)


# Depth range
min_depth = float(df["depth_km"].min())
max_depth = float(df["depth_km"].max())

selected_depth_range = st.sidebar.slider(
    "📏 Depth Range (km)",
    min_value=min_depth,
    max_value=max_depth,
    value=(min_depth, max_depth)
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    (df["year"].isin(selected_years)) &
    (df["magnitude_category"].isin(selected_categories)) &
    (df["type"].isin(selected_types)) &
    (df["tsunami"].isin(selected_tsunami)) &
    (df["mag"].between(
        selected_mag_range[0],
        selected_mag_range[1]
    )) &
    (df["depth_km"].between(
        selected_depth_range[0],
        selected_depth_range[1]
    ))
].copy()


if selected_countries:

    filtered_df = filtered_df[
        filtered_df["country"].isin(selected_countries)
    ]


# ============================================================
# KEY STATISTICS
# ============================================================

total_events = len(filtered_df)

if total_events > 0:

    average_magnitude = filtered_df["mag"].mean()

    maximum_magnitude = filtered_df["mag"].max()

    minimum_magnitude = filtered_df["mag"].min()

    strong_major_events = filtered_df[
        filtered_df["magnitude_category"].isin(
            ["Strong", "Major"]
        )
    ].shape[0]

else:

    average_magnitude = 0
    maximum_magnitude = 0
    minimum_magnitude = 0
    strong_major_events = 0


# ============================================================
# KEY STATISTICS DISPLAY
# ============================================================

st.header("📊 Key Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Events",
        f"{total_events:,}"
    )

with col2:
    st.metric(
        "Average Magnitude",
        f"{average_magnitude:.2f}"
    )

with col3:
    st.metric(
        "Maximum Magnitude",
        f"{maximum_magnitude:.1f}"
    )

with col4:
    st.metric(
        "Strong / Major Events",
        f"{strong_major_events:,}"
    )

st.divider()


# ============================================================
# EVENTS BY YEAR
# ============================================================

st.header("📈 Earthquake Events by Year")

if len(filtered_df) > 0:

    yearly_events = (
        filtered_df
        .groupby("year")
        .size()
        .reset_index(name="Earthquakes")
        .sort_values("year")
    )

    st.bar_chart(
        yearly_events.set_index("year")["Earthquakes"],
        width="stretch"
    )

else:

    st.warning(
        "No data available for the selected filters."
    )


# ============================================================
# EVENTS BY MONTH
# ============================================================

st.header("📅 Earthquake Events by Month")

if len(filtered_df) > 0:

    monthly_events = (
        filtered_df
        .groupby("month")
        .size()
        .reset_index(name="Earthquakes")
        .sort_values("month")
    )

    st.line_chart(
        monthly_events.set_index("month")["Earthquakes"],
        width="stretch"
    )


# ============================================================
# MAGNITUDE CATEGORY & EVENT TYPE
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📊 Magnitude Category")

    if len(filtered_df) > 0:

        category_events = (
            filtered_df
            .groupby("magnitude_category")
            .size()
            .reset_index(name="Earthquakes")
            .sort_values(
                "Earthquakes",
                ascending=False
            )
        )

        st.bar_chart(
            category_events.set_index(
                "magnitude_category"
            )["Earthquakes"],
            width="stretch"
        )


with col2:

    st.subheader("🌋 Event Type")

    if len(filtered_df) > 0:

        type_events = (
            filtered_df
            .groupby("type")
            .size()
            .reset_index(name="Events")
            .sort_values(
                "Events",
                ascending=False
            )
            .head(10)
        )

        st.bar_chart(
            type_events.set_index("type")["Events"],
            width="stretch"
        )


# ============================================================
# MAGNITUDE DISTRIBUTION
# ============================================================

st.divider()

st.header("📉 Magnitude Distribution")

if len(filtered_df) > 0:

    magnitude_data = (
        filtered_df[["mag"]]
        .dropna()
        .sort_values("mag")
        .reset_index(drop=True)
    )

    st.line_chart(
        magnitude_data,
        width="stretch"
    )


# ============================================================
# TSUNAMI EVENTS
# ============================================================

st.header("🌊 Tsunami Events")

if len(filtered_df) > 0:

    tsunami_counts = (
        filtered_df
        .groupby("tsunami")
        .size()
        .reset_index(name="Events")
    )

    st.bar_chart(
        tsunami_counts.set_index("tsunami")["Events"],
        width="stretch"
    )


# ============================================================
# GLOBAL EARTHQUAKE MAP
# ============================================================

st.divider()

st.header("🌍 Global Earthquake Map")

if len(filtered_df) > 0:

    map_data = filtered_df[
        ["latitude", "longitude", "mag"]
    ].dropna()

    if len(map_data) > 10000:

        map_data = map_data.sample(
            10000,
            random_state=42
        )

    st.map(
        map_data,
        latitude="latitude",
        longitude="longitude",
        size="mag"
    )

    st.caption(
        "Map displays earthquake locations. "
        "Larger points represent higher-magnitude events."
    )


# ============================================================
# STRONGEST EARTHQUAKES
# ============================================================

st.divider()

st.header("🚨 Strongest Earthquakes")

if len(filtered_df) > 0:

    top_earthquakes = (
        filtered_df
        .sort_values(
            "mag",
            ascending=False
        )[
            [
                "date",
                "mag",
                "magnitude_category",
                "place",
                "latitude",
                "longitude",
                "depth_km",
                "tsunami"
            ]
        ]
        .head(20)
    )

    st.dataframe(
        top_earthquakes,
        width="stretch"
    )

import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Global Seismic Trends",
    page_icon="🌍",
    layout="wide"
)

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    file_path = "data/cleaned_seismic_data.csv"

    df = pd.read_csv(file_path)

    # Convert date
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    elif "time" in df.columns:
        df["date"] = pd.to_datetime(df["time"], errors="coerce")

    # Create time-related columns if missing
    if "year" not in df.columns:
        df["year"] = df["date"].dt.year

    if "month" not in df.columns:
        df["month"] = df["date"].dt.month

    if "hour" not in df.columns:
        df["hour"] = df["date"].dt.hour

    if "day_of_week" not in df.columns:
        df["day_of_week"] = df["date"].dt.day_name()

    # Numeric columns
    numeric_columns = [
        "latitude",
        "longitude",
        "depth_km",
        "mag",
        "tsunami",
        "nst",
        "rms",
        "gap",
        "year",
        "month",
        "hour"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


try:
    df = load_data()

except Exception as e:
    st.error("Unable to load the earthquake dataset.")
    st.error(str(e))
    st.stop()


# ============================================================
# TITLE
# ============================================================

st.title("🌍 Global Seismic Trends")
st.subheader("Data-Driven Earthquake Insights")

st.write(
    "Interactive analysis of global earthquake activity using "
    "USGS earthquake data, Python, SQL and Streamlit."
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")

# Year
if "year" in df.columns:
    years = sorted(df["year"].dropna().unique().astype(int))

    selected_years = st.sidebar.multiselect(
        "Year",
        years,
        default=years
    )
else:
    selected_years = []


# Magnitude category
if "magnitude_category" in df.columns:
    categories = sorted(
        df["magnitude_category"].dropna().unique().tolist()
    )

    selected_categories = st.sidebar.multiselect(
        "Magnitude Category",
        categories,
        default=categories
    )
else:
    selected_categories = []


# Event type
if "type" in df.columns:
    event_types = sorted(
        df["type"].dropna().unique().tolist()
    )

    selected_types = st.sidebar.multiselect(
        "Event Type",
        event_types,
        default=event_types
    )
else:
    selected_types = []


# Tsunami
if "tsunami" in df.columns:
    tsunami_option = st.sidebar.selectbox(
        "Tsunami",
        ["All", "Yes", "No"]
    )
else:
    tsunami_option = "All"


# Country
if "country" in df.columns:
    countries = sorted(
        df["country"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_countries = st.sidebar.multiselect(
        "Country",
        countries
    )
else:
    selected_countries = []


# Magnitude range
if "mag" in df.columns:
    min_mag = float(df["mag"].min())
    max_mag = float(df["mag"].max())

    magnitude_range = st.sidebar.slider(
        "Magnitude Range",
        min_value=min_mag,
        max_value=max_mag,
        value=(min_mag, max_mag),
        step=0.1
    )
else:
    magnitude_range = (0.0, 10.0)


# Depth range
if "depth_km" in df.columns:
    min_depth = float(df["depth_km"].min())
    max_depth = float(df["depth_km"].max())

    depth_range = st.sidebar.slider(
        "Depth Range (km)",
        min_value=min_depth,
        max_value=max_depth,
        value=(min_depth, max_depth),
        step=1.0
    )
else:
    depth_range = (-10.0, 700.0)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if selected_years and "year" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["year"].isin(selected_years)
    ]

if selected_categories and "magnitude_category" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["magnitude_category"].isin(selected_categories)
    ]

if selected_types and "type" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["type"].isin(selected_types)
    ]

if selected_countries and "country" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["country"].isin(selected_countries)
    ]

if "mag" in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df["mag"] >= magnitude_range[0]) &
        (filtered_df["mag"] <= magnitude_range[1])
    ]

if "depth_km" in filtered_df.columns:
    filtered_df = filtered_df[
        (filtered_df["depth_km"] >= depth_range[0]) &
        (filtered_df["depth_km"] <= depth_range[1])
    ]

if tsunami_option == "Yes" and "tsunami" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["tsunami"] == 1
    ]

elif tsunami_option == "No" and "tsunami" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["tsunami"] == 0
    ]


# ============================================================
# KPI SECTION
# ============================================================

st.header("📊 Key Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Events",
        f"{len(filtered_df):,}"
    )

with col2:
    if len(filtered_df) > 0:
        st.metric(
            "Average Magnitude",
            f"{filtered_df['mag'].mean():.2f}"
        )
    else:
        st.metric("Average Magnitude", "N/A")

with col3:
    if len(filtered_df) > 0:
        st.metric(
            "Maximum Magnitude",
            f"{filtered_df['mag'].max():.1f}"
        )
    else:
        st.metric("Maximum Magnitude", "N/A")

with col4:
    if "magnitude_category" in filtered_df.columns:
        strong_major = filtered_df[
            filtered_df["magnitude_category"].isin(
                ["Strong", "Major"]
            )
        ]

        st.metric(
            "Strong / Major Events",
            f"{len(strong_major):,}"
        )
    else:
        st.metric("Strong / Major Events", "N/A")


st.divider()


# ============================================================
# YEARLY TREND
# ============================================================

st.header("📈 Earthquake Trends")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Earthquakes by Year")

    if len(filtered_df) > 0:

        yearly = (
            filtered_df
            .groupby("year")
            .size()
            .sort_index()
        )

        st.bar_chart(yearly)

    else:
        st.info("No data available for the selected filters.")


# ============================================================
# MONTHLY TREND
# ============================================================

with col2:

    st.subheader("Earthquakes by Month")

    if len(filtered_df) > 0:

        monthly = (
            filtered_df
            .groupby("month")
            .size()
            .sort_index()
        )

        st.bar_chart(monthly)

    else:
        st.info("No data available.")


# ============================================================
# MAGNITUDE & EVENT TYPE
# ============================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("Magnitude Categories")

    if "magnitude_category" in filtered_df.columns:

        magnitude_counts = (
            filtered_df["magnitude_category"]
            .value_counts()
        )

        st.bar_chart(magnitude_counts)

with col2:

    st.subheader("Event Types")

    if "type" in filtered_df.columns:

        type_counts = (
            filtered_df["type"]
            .value_counts()
            .head(10)
        )

        st.bar_chart(type_counts)


# ============================================================
# MAGNITUDE DISTRIBUTION
# ============================================================

st.subheader("Magnitude Distribution")

if len(filtered_df) > 0:

    magnitude_hist = pd.cut(
        filtered_df["mag"],
        bins=20
    ).value_counts().sort_index()

    magnitude_hist.index = magnitude_hist.index.astype(str)

    st.bar_chart(magnitude_hist)


# ============================================================
# TSUNAMI ANALYSIS
# ============================================================

st.subheader("🌊 Tsunami Events")

if "tsunami" in filtered_df.columns:

    tsunami_counts = (
        filtered_df["tsunami"]
        .value_counts()
        .rename(index={
            0: "No Tsunami",
            1: "Tsunami"
        })
    )

    st.bar_chart(tsunami_counts)


# ============================================================
# GLOBAL MAP
# ============================================================

st.header("🌎 Global Earthquake Map")

if (
    "latitude" in filtered_df.columns and
    "longitude" in filtered_df.columns
):

    map_df = filtered_df[
        ["latitude", "longitude"]
    ].dropna()

    # Limit points for better performance
    if len(map_df) > 10000:
        map_df = map_df.sample(
            10000,
            random_state=42
        )

    st.map(map_df)

else:
    st.info("Latitude and longitude information unavailable.")


# ============================================================
# STRONGEST EARTHQUAKES
# ============================================================

st.header("🔥 Strongest Earthquakes")

if len(filtered_df) > 0:

    strongest_columns = [
        "date",
        "mag",
        "place",
        "depth_km",
        "latitude",
        "longitude"
    ]

    available_columns = [
        col for col in strongest_columns
        if col in filtered_df.columns
    ]

    strongest = (
        filtered_df[
            available_columns
        ]
        .sort_values(
            "mag",
            ascending=False
        )
        .head(10)
    )

    st.dataframe(
        strongest,
        use_container_width=True
    )


# ============================================================
# 30 SQL / ANALYTICAL QUESTIONS
# ============================================================

st.divider()

st.header("🔎 Analytical Questions – 30 Questions")

questions = [

    "Q1 – Top 10 strongest earthquakes",

    "Q2 – Top 10 deepest earthquakes",

    "Q3 – Shallow earthquakes with magnitude > 7.5",

    "Q4 – Average depth per continent",

    "Q5 – Average magnitude by magnitude type",

    "Q6 – Year with the most earthquakes",

    "Q7 – Month with the highest number of earthquakes",

    "Q8 – Day of week with the most earthquakes",

    "Q9 – Earthquake count by hour",

    "Q10 – Most active reporting network",

    "Q11 – Top 5 places with highest casualties",

    "Q12 – Economic loss per continent",

    "Q13 – Economic loss by alert level",

    "Q14 – Reviewed vs automatic earthquakes",

    "Q15 – Earthquake count by type",

    "Q16 – Earthquake count by data type",

    "Q17 – Average RMS and gap per continent",

    "Q18 – Events with high station coverage",

    "Q19 – Tsunami events per year",

    "Q20 – Earthquake count by alert level",

    "Q21 – Top 5 countries by average magnitude",

    "Q22 – Countries with both shallow and deep earthquakes",

    "Q23 – Year-over-year earthquake growth",

    "Q24 – Top 3 seismically active regions",

    "Q25 – Average depth near the equator",

    "Q26 – Countries with highest shallow/deep ratio",

    "Q27 – Tsunami vs non-tsunami magnitude",

    "Q28 – Lowest data reliability",

    "Q29 – Consecutive earthquakes within 50 km and 1 hour",

    "Q30 – Regions with most deep-focus earthquakes"
]

selected_question = st.selectbox(
    "Select an analytical question:",
    questions
)

st.write("")


# ============================================================
# Q1
# ============================================================

if selected_question.startswith("Q1"):

    st.subheader("Q1 – Top 10 Strongest Earthquakes")

    result = (
        filtered_df
        .sort_values("mag", ascending=False)
        .head(10)
    )

    st.dataframe(
        result,
        use_container_width=True
    )


# ============================================================
# Q2
# ============================================================

elif selected_question.startswith("Q2"):

    st.subheader("Q2 – Top 10 Deepest Earthquakes")

    result = (
        filtered_df
        .sort_values("depth_km", ascending=False)
        .head(10)
    )

    st.dataframe(
        result,
        use_container_width=True
    )


# ============================================================
# Q3
# ============================================================

elif selected_question.startswith("Q3"):

    st.subheader(
        "Q3 – Shallow Earthquakes with Magnitude > 7.5"
    )

    result = filtered_df[
        (filtered_df["depth_km"] < 50) &
        (filtered_df["mag"] > 7.5)
    ]

    st.dataframe(
        result,
        use_container_width=True
    )

    st.metric("Number of Events", len(result))


# ============================================================
# Q4
# ============================================================

elif selected_question.startswith("Q4"):

    st.subheader("Q4 – Average Depth per Continent")

    st.warning(
        "This analysis cannot be calculated directly because "
        "the USGS dataset does not contain a standardized continent column."
    )


# ============================================================
# Q5
# ============================================================

elif selected_question.startswith("Q5"):

    st.subheader("Q5 – Average Magnitude by Magnitude Type")

    result = (
        filtered_df
        .groupby("magType")["mag"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(result)

    st.dataframe(
        result.reset_index(name="average_magnitude"),
        use_container_width=True
    )


# ============================================================
# Q6
# ============================================================

elif selected_question.startswith("Q6"):

    st.subheader("Q6 – Year with Most Earthquakes")

    result = (
        filtered_df
        .groupby("year")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(result)

    if len(result) > 0:
        st.success(
            f"Year with the most earthquakes: "
            f"{result.index[0]} ({result.iloc[0]:,} events)"
        )


# ============================================================
# Q7
# ============================================================

elif selected_question.startswith("Q7"):

    st.subheader("Q7 – Month with Highest Number of Earthquakes")

    result = (
        filtered_df
        .groupby("month")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(result)

    if len(result) > 0:
        st.success(
            f"Month with the highest activity: "
            f"{result.index[0]} ({result.iloc[0]:,} events)"
        )


# ============================================================
# Q8
# ============================================================

elif selected_question.startswith("Q8"):

    st.subheader("Q8 – Earthquakes by Day of Week")

    result = (
        filtered_df
        .groupby("day_of_week")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(result)

    st.dataframe(
        result.reset_index(name="earthquake_count"),
        use_container_width=True
    )


# ============================================================
# Q9
# ============================================================

elif selected_question.startswith("Q9"):

    st.subheader("Q9 – Earthquake Count by Hour")

    result = (
        filtered_df
        .groupby("hour")
        .size()
        .sort_index()
    )

    st.line_chart(result)

    st.dataframe(
        result.reset_index(name="earthquake_count"),
        use_container_width=True
    )


# ============================================================
# Q10
# ============================================================

elif selected_question.startswith("Q10"):

    st.subheader("Q10 – Most Active Reporting Network")

    result = (
        filtered_df["net"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(result)

    if len(result) > 0:
        st.success(
            f"Most active network: {result.index[0]}"
        )


# ============================================================
# Q11
# ============================================================

elif selected_question.startswith("Q11"):

    st.subheader("Q11 – Places with Highest Casualties")

    st.warning(
        "Casualty information is not available in the USGS dataset "
        "used for this project."
    )


# ============================================================
# Q12
# ============================================================

elif selected_question.startswith("Q12"):

    st.subheader("Q12 – Economic Loss per Continent")

    st.warning(
        "Economic loss and standardized continent information "
        "are not available in the project dataset."
    )


# ============================================================
# Q13
# ============================================================

elif selected_question.startswith("Q13"):

    st.subheader("Q13 – Economic Loss by Alert Level")

    st.warning(
        "Economic loss and the required alert-level data "
        "are not available in the project dataset."
    )


# ============================================================
# Q14
# ============================================================

elif selected_question.startswith("Q14"):

    st.subheader("Q14 – Reviewed vs Automatic Earthquakes")

    result = (
        filtered_df["status"]
        .value_counts()
    )

    st.bar_chart(result)

    st.dataframe(
        result.reset_index(name="count"),
        use_container_width=True
    )


# ============================================================
# Q15
# ============================================================

elif selected_question.startswith("Q15"):

    st.subheader("Q15 – Earthquake Count by Type")

    result = (
        filtered_df["type"]
        .value_counts()
    )

    st.bar_chart(result)


# ============================================================
# Q16
# ============================================================

elif selected_question.startswith("Q16"):

    st.subheader("Q16 – Earthquake Count by Data Type")

    result = (
        filtered_df["types"]
        .value_counts()
        .head(15)
    )

    st.bar_chart(result)

    st.dataframe(
        result.reset_index(name="count"),
        use_container_width=True
    )


# ============================================================
# Q17
# ============================================================

elif selected_question.startswith("Q17"):

    st.subheader("Q17 – Average RMS and Gap per Continent")

    st.warning(
        "A standardized continent column is not available "
        "in the project dataset."
    )


# ============================================================
# Q18
# ============================================================

elif selected_question.startswith("Q18"):

    st.subheader("Q18 – Events with High Station Coverage")

    threshold = st.number_input(
        "NST Threshold",
        min_value=1,
        value=100,
        step=10
    )

    result = filtered_df[
        filtered_df["nst"] > threshold
    ]

    st.metric(
        "Events above threshold",
        f"{len(result):,}"
    )

    st.dataframe(
        result,
        use_container_width=True
    )


# ============================================================
# Q19
# ============================================================

elif selected_question.startswith("Q19"):

    st.subheader("Q19 – Tsunami Events per Year")

    result = (
        filtered_df[
            filtered_df["tsunami"] == 1
        ]
        .groupby("year")
        .size()
        .sort_index()
    )

    st.bar_chart(result)

    st.dataframe(
        result.reset_index(name="tsunami_events"),
        use_container_width=True
    )


# ============================================================
# Q20
# ============================================================

elif selected_question.startswith("Q20"):

    st.subheader("Q20 – Earthquake Count by Alert Level")

    st.warning(
        "Alert-level information is not available "
        "in the project dataset."
    )


# ============================================================
# Q21
# ============================================================

elif selected_question.startswith("Q21"):

    st.subheader(
        "Q21 – Top 5 Countries by Average Magnitude"
    )

    result = (
        filtered_df
        .dropna(subset=["country", "mag"])
        .groupby("country")
        .agg(
            average_magnitude=("mag", "mean"),
            event_count=("mag", "count")
        )
    )

    result = result[
        result["event_count"] >= 100
    ]

    result = result.sort_values(
        "average_magnitude",
        ascending=False
    ).head(5)

    st.bar_chart(
        result["average_magnitude"]
    )

    st.dataframe(
        result.reset_index(),
        use_container_width=True
    )


# ============================================================
# Q22
# ============================================================

elif selected_question.startswith("Q22"):

    st.subheader(
        "Q22 – Countries with Both Shallow and Deep Earthquakes"
    )

    temp = filtered_df.copy()

    temp["depth_group"] = np.where(
        temp["depth_km"] < 50,
        "Shallow",
        "Deep"
    )

    result = (
        temp
        .groupby(["country", "year", "month"])["depth_group"]
        .nunique()
        .reset_index(name="depth_group_count")
    )

    result = result[
        result["depth_group_count"] == 2
    ]

    st.dataframe(
        result,
        use_container_width=True
    )


# ============================================================
# Q23
# ============================================================

elif selected_question.startswith("Q23"):

    st.subheader(
        "Q23 – Year-over-Year Earthquake Growth"
    )

    yearly = (
        filtered_df
        .groupby("year")
        .size()
        .sort_index()
    )

    yoy = yearly.pct_change() * 100

    result = pd.DataFrame({
        "year": yearly.index,
        "earthquake_count": yearly.values,
        "YoY_growth_percent": yoy.values
    })

    st.line_chart(
        result.set_index("year")[
            "YoY_growth_percent"
        ]
    )

    st.dataframe(
        result,
        use_container_width=True
    )


# ============================================================
# Q24
# ============================================================

elif selected_question.startswith("Q24"):

    st.subheader(
        "Q24 – Top 3 Seismically Active Regions"
    )

    st.info(
        "Because the dataset does not contain a standardized "
        "region field, country is used as the regional proxy."
    )

    result = (
        filtered_df
        .dropna(subset=["country", "mag"])
        .groupby("country")
        .agg(
            frequency=("mag", "count"),
            average_magnitude=("mag", "mean")
        )
    )

    result = result[
        result["frequency"] >= 100
    ]

    result["frequency_rank"] = (
        result["frequency"]
        .rank(ascending=False)
    )

    result["magnitude_rank"] = (
        result["average_magnitude"]
        .rank(ascending=False)
    )

    result["combined_rank"] = (
        result["frequency_rank"] +
        result["magnitude_rank"]
    )

    result = result.sort_values(
        "combined_rank"
    ).head(3)

    st.dataframe(
        result.reset_index(),
        use_container_width=True
    )


# ============================================================
# Q25
# ============================================================

elif selected_question.startswith("Q25"):

    st.subheader(
        "Q25 – Average Depth Near the Equator"
    )

    result = (
        filtered_df[
            filtered_df["latitude"].between(-5, 5)
        ]
        .dropna(subset=["country", "depth_km"])
        .groupby("country")["depth_km"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(result.head(15))

    st.dataframe(
        result.reset_index(
            name="average_depth_km"
        ),
        use_container_width=True
    )


# ============================================================
# Q26
# ============================================================

elif selected_question.startswith("Q26"):

    st.subheader(
        "Q26 – Countries with Highest Shallow/Deep Ratio"
    )

    temp = filtered_df.copy()

    shallow = (
        temp[temp["depth_km"] < 50]
        .groupby("country")
        .size()
    )

    deep = (
        temp[temp["depth_km"] >= 50]
        .groupby("country")
        .size()
    )

    result = pd.DataFrame({
        "shallow_count": shallow,
        "deep_count": deep
    }).fillna(0)

    result = result[
        result["deep_count"] > 0
    ]

    result["shallow_deep_ratio"] = (
        result["shallow_count"] /
        result["deep_count"]
    )

    result = result.sort_values(
        "shallow_deep_ratio",
        ascending=False
    ).head(10)

    st.bar_chart(
        result["shallow_deep_ratio"]
    )

    st.dataframe(
        result.reset_index(),
        use_container_width=True
    )


# ============================================================
# Q27
# ============================================================

elif selected_question.startswith("Q27"):

    st.subheader(
        "Q27 – Tsunami vs Non-Tsunami Average Magnitude"
    )

    result = (
        filtered_df
        .groupby("tsunami")["mag"]
        .mean()
        .rename(
            index={
                0: "No Tsunami",
                1: "Tsunami"
            }
        )
    )

    st.bar_chart(result)

    st.dataframe(
        result.reset_index(
            name="average_magnitude"
        ),
        use_container_width=True
    )


# ============================================================
# Q28
# ============================================================

elif selected_question.startswith("Q28"):

    st.subheader(
        "Q28 – Lowest Data Reliability"
    )

    st.info(
        "This is a project-defined reliability score using "
        "GAP and RMS. It is not an official USGS reliability score."
    )

    result = (
        filtered_df
        .dropna(subset=["country", "gap", "rms"])
        .groupby("country")
        .agg(
            average_gap=("gap", "mean"),
            average_rms=("rms", "mean"),
            event_count=("gap", "count")
        )
    )

    result = result[
        result["event_count"] >= 100
    ]

    if len(result) > 0:

        result["reliability_score"] = (
            result["average_gap"] /
            result["average_gap"].max()
            +
            result["average_rms"] /
            result["average_rms"].max()
        )

        result = result.sort_values(
            "reliability_score",
            ascending=False
        ).head(10)

        st.bar_chart(
            result["reliability_score"]
        )

        st.dataframe(
            result.reset_index(),
            use_container_width=True
        )


# ============================================================
# Q29
# ============================================================

elif selected_question.startswith("Q29"):

    st.subheader(
        "Q29 – Consecutive Earthquakes Within 50 km and 1 Hour"
    )

    st.info(
        "The calculation compares each earthquake with the "
        "immediately preceding earthquake after sorting by time."
    )

    required = [
        "date",
        "latitude",
        "longitude",
        "mag",
        "place"
    ]

    if all(col in filtered_df.columns for col in required):

        temp = (
            filtered_df[
                required
            ]
            .dropna()
            .sort_values("date")
            .reset_index(drop=True)
        )

        if len(temp) >= 2:

            lat1 = np.radians(
                temp["latitude"]
            )

            lon1 = np.radians(
                temp["longitude"]
            )

            lat2 = lat1.shift(1)
            lon2 = lon1.shift(1)

            dlat = lat1 - lat2
            dlon = lon1 - lon2

            a = (
                np.sin(dlat / 2) ** 2
                +
                np.cos(lat1)
                * np.cos(lat2)
                * np.sin(dlon / 2) ** 2
            )

            distance = (
                6371
                * 2
                * np.arcsin(
                    np.sqrt(a)
                )
            )

            time_difference = (
                temp["date"]
                .diff()
                .dt.total_seconds()
                / 3600
            )

            temp["distance_km"] = distance
            temp["time_difference_hours"] = time_difference

            result = temp[
                (temp["distance_km"] <= 50) &
                (temp["time_difference_hours"] <= 1)
            ]

            st.metric(
                "Matching consecutive pairs",
                f"{len(result):,}"
            )

            st.dataframe(
                result,
                use_container_width=True
            )

        else:
            st.info("Not enough events to calculate pairs.")

    else:
        st.warning(
            "Required location/time columns are not available."
        )


# ============================================================
# Q30
# ============================================================

elif selected_question.startswith("Q30"):

    st.subheader(
        "Q30 – Deep-Focus Earthquakes (>300 km)"
    )

    result = (
        filtered_df[
            filtered_df["depth_km"] > 300
        ]
        .dropna(subset=["country"])
        .groupby("country")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(result)

    st.dataframe(
        result.reset_index(
            name="deep_focus_events"
        ),
        use_container_width=True
    )


# ============================================================
# FILTERED DATA
# ============================================================

st.divider()

st.header("📋 Filtered Dataset")

st.write(
    f"Showing {len(filtered_df):,} records."
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Global Seismic Trends | USGS Earthquake Data | Python + Pandas + SQL + Streamlit"
)