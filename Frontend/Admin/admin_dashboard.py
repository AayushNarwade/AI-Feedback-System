import streamlit as st
import requests
import pandas as pd
import altair as alt

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

# Convert timestamp column
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ----------------------------------------------
#  BEAUTIFUL SUMMARY CARDS
# ----------------------------------------------

st.markdown("### 📊 Overview")

col1, col2, col3 = st.columns(3)

total_submissions = len(df)
average_rating = round(df["rating"].mean(), 2)
latest_date = df["timestamp"].max().strftime("%d %b %Y")

col1.metric("Total Submissions", total_submissions)
col2.metric("Average Rating", average_rating)
col3.metric("Last Submission", latest_date)

st.markdown("---")

# ----------------------------------------------
#  RATING DISTRIBUTION — Clean Altair Chart
# ----------------------------------------------

st.markdown("### ⭐ Rating Distribution")

rating_counts = (
    df.groupby("rating").size().reset_index(name="count")
)

rating_chart = (
    alt.Chart(rating_counts)
    .mark_bar(color="#4CAF50")
    .encode(
        x=alt.X("rating:O", title="Rating"),
        y=alt.Y("count:Q", title="Number of Submissions"),
        tooltip=["rating", "count"]
    )
)

st.altair_chart(rating_chart, use_container_width=True)

st.markdown("---")

# ----------------------------------------------
#  AVERAGE RATING OVER TIME — Smooth Line Chart
# ----------------------------------------------

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

# ----------------------------------------------
#  SUBMISSIONS PER DAY — Clean Bar Chart
# ----------------------------------------------

st.markdown("### 🗓 Submissions Per Day")

daily_counts = (
    df.groupby(df["timestamp"].dt.date).size().reset_index(name="count")
)

daily_chart = (
    alt.Chart(daily_counts)
    .mark_area(color="#FF9800")
    .encode(
        x=alt.X("timestamp:T", title="Date"),
        y=alt.Y("count:Q", title="Submissions"),
        tooltip=["timestamp", "count"]
    )
)

st.altair_chart(daily_chart, use_container_width=True)

st.markdown("---")

# ----------------------------------------------
#  TOP REVIEW KEYWORDS — Professional Horizontal Bar Chart
# ----------------------------------------------

st.markdown("### 🔍 Top Keywords from Reviews")

import re
from collections import Counter

def extract_keywords(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    stopwords = {"the", "is", "was", "and", "to", "it", "of", "in", "for", "very", "a", "an", "this", "that"}
    return [w for w in words if w not in stopwords and len(w) > 3]

keywords = []
for review in df["review"]:
    keywords.extend(extract_keywords(review))

if len(keywords) > 0:
    word_counts = Counter(keywords).most_common(8)
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
    st.info("Not enough review data for keyword insights.")

st.markdown("---")

# ----------------------------------------------
#  RAW TABLE (Well-Formatted)
# ----------------------------------------------

st.markdown("### 📋 All Submissions (Detailed Table)")
st.dataframe(df, use_container_width=True)
