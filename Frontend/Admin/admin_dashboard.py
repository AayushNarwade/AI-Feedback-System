import streamlit as st
import requests
import pandas as pd
import altair as alt
from collections import Counter
import re

# Replace with your deployed backend URL
BACKEND_URL = "https://ai-feedback-system-47yp.onrender.com"

st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("🛠 Admin Dashboard")

# Load submissions
try:
    submissions = requests.get(BACKEND_URL + "/submissions").json()
    df = pd.DataFrame(submissions)
except:
    st.error("Unable to fetch data from backend.")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"])  # convert timestamp

# -------------------------------------------------------------
# 🔷 HEADER METRICS
# -------------------------------------------------------------

st.markdown("### 📊 Overview")

col1, col2, col3 = st.columns(3)

total_submissions = len(df)
average_rating = round(df["rating"].mean(), 2)
latest_date = df["timestamp"].max().strftime("%d %b %Y")

col1.metric("Total Submissions", total_submissions)
col2.metric("Average Rating", average_rating)
col3.metric("Last Submission", latest_date)

st.markdown("---")

# -------------------------------------------------------------
# 🟣 PIE CHART — RATING DISTRIBUTION (DONUT)
# -------------------------------------------------------------

st.markdown("### 🍩 Rating Distribution (Pie Chart)")

rating_counts = (
    df.groupby("rating").size().reset_index(name="count")
)

rating_counts["percentage"] = (rating_counts["count"] / rating_counts["count"].sum()) * 100

pie_chart = (
    alt.Chart(rating_counts)
    .mark_arc(innerRadius=50)
    .encode(
        theta=alt.Theta("count:Q", title="Count"),
        color=alt.Color("rating:N", title="Rating"),
        tooltip=["rating", "count", "percentage"]
    )
)

st.altair_chart(pie_chart, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------
# 📈 RATING TREND — LINE CHART
# -------------------------------------------------------------

st.markdown("### 📈 Rating Trend Over Time")

rating_over_time = (
    df.groupby(df["timestamp"].dt.date)["rating"]
    .mean()
    .reset_index(name="avg_rating")
)

line_chart = (
    alt.Chart(rating_over_time)
    .mark_line(point=True, color="#2196F3")
    .encode(
        x=alt.X("timestamp:T", title="Date"),
        y=alt.Y("avg_rating:Q", title="Average Rating"),
        tooltip=["timestamp", "avg_rating"]
    )
)

st.altair_chart(line_chart, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------
# 🔍 TOP KEYWORDS — BAR CHART
# -------------------------------------------------------------

st.markdown("### 🔍 Top Keywords in Reviews")

def extract_keywords(text):
    text = re.sub(r"[^a-zA-Z\s]", "", text.lower())
    words = text.split()
    stops = {"the", "is", "was", "and", "to", "it", "of", "in", "for", "very", "a", "an", "this", "that"}
    return [w for w in words if w not in stops and len(w) > 3]

keywords = []
for review in df["review"]:
    keywords.extend(extract_keywords(review))

if len(keywords) > 0:
    word_counts = Counter(keywords).most_common(10)
    keyword_df = pd.DataFrame(word_counts, columns=["keyword", "count"])

    keyword_chart = (
        alt.Chart(keyword_df)
        .mark_bar(color="#9C27B0")
        .encode(
            x=alt.X("count:Q", title="Frequency"),
            y=alt.Y("keyword:O", sort="-x", title="Keyword"),
            tooltip=["keyword", "count"]
        )
    )
    
    st.altair_chart(keyword_chart, use_container_width=True)
else:
    st.info("Not enough data for keyword analysis.")

st.markdown("---")

# -------------------------------------------------------------
# 📋 CLEAN TABLE — ONLY SELECTED COLUMNS
# -------------------------------------------------------------

st.markdown("### 📋 User Feedback Table")

clean_df = df[[
    "id",
    "rating",
    "review",
    "ai_summary",
    "ai_actions"
]].rename(columns={
    "id": "User ID",
    "rating": "User Rating",
    "review": "User Review",
    "ai_summary": "AI Summary",
    "ai_actions": "Recommended Actions"
})

st.dataframe(clean_df, use_container_width=True)
