import streamlit as st
import requests
import pandas as pd
import altair as alt

BACKEND_URL = "https://ai-feedback-system-47yp.onrender.com"

st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("🛠 Admin Dashboard")

try:
    submissions = requests.get(BACKEND_URL + "/submissions").json()
    df = pd.DataFrame(submissions)
except:
    st.error("Unable to fetch data from backend.")
    st.stop()

df["timestamp"] = pd.to_datetime(df["timestamp"])

st.markdown("### 📊 Overview")

col1, col2, col3 = st.columns(3)

total_submissions = len(df)
average_rating = round(df["rating"].mean(), 2)
latest_date = df["timestamp"].max().strftime("%d %b %Y")

col1.metric("Total Submissions", total_submissions)
col2.metric("Average Rating", average_rating)
col3.metric("Last Submission", latest_date)

st.markdown("---")

st.markdown("### ⭐ Ratings Breakdown & Trend")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("####  Rating Distribution (Donut Chart)")

    rating_counts = df.groupby("rating").size().reset_index(name="count")
    rating_counts["percentage"] = rating_counts["count"] / rating_counts["count"].sum() * 100

    color_scale = alt.Scale(
        domain=[1, 2, 3, 4, 5],
        range=["#d32f2f", "#f57c00", "#ffca28", "#66bb6a", "#2e7d32"]
    )

    pie_chart = (
        alt.Chart(rating_counts)
        .mark_arc(innerRadius=50)
        .encode(
            theta="count:Q",
            color=alt.Color("rating:N", scale=color_scale, title="Rating"),
            tooltip=["rating", "count", alt.Tooltip("percentage:Q", format=".1f")]
        )
    )

    st.altair_chart(pie_chart, use_container_width=True)

with col_right:
    st.markdown("#### 📈 Rating Trend Over Time")

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
            y=alt.Y("avg_rating:Q", title="Average Rating (Daily Mean)"),
            tooltip=["timestamp", "avg_rating"]
        )
        .properties(height=350)
    )

    st.altair_chart(line_chart, use_container_width=True)

st.markdown("---")

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
