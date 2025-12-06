import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
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

st.subheader("📋 All Submissions")
st.dataframe(df, use_container_width=True)

# --------------------------------------------------------------------------------
# 📊 Section: Basic Analytics
# --------------------------------------------------------------------------------

try:
    analytics = requests.get(BACKEND_URL + "/analytics").json()
    st.subheader("📊 Basic Analytics")

    col1, col2 = st.columns(2)
    if "total_submissions" in analytics:
        col1.metric("Total Submissions", analytics["total_submissions"])
        col2.metric("Average Rating", round(analytics["avg_rating"], 2))
    else:
        st.warning("Analytics unavailable")

except:
    st.error("Error loading analytics.")

# --------------------------------------------------------------------------------
# 📊 Rating Distribution
# --------------------------------------------------------------------------------

st.subheader("⭐ Rating Distribution")

fig, ax = plt.subplots()
df["rating"].value_counts().sort_index().plot(kind="bar", ax=ax)
ax.set_title("Distribution of User Ratings")
ax.set_xlabel("Rating")
ax.set_ylabel("Count")
st.pyplot(fig)

# --------------------------------------------------------------------------------
# 📈 Ratings Over Time
# --------------------------------------------------------------------------------

if "timestamp" in df:
    st.subheader("📈 Average Rating Over Time")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df_sorted = df.sort_values("timestamp")

    df_sorted["rolling_avg"] = df_sorted["rating"].rolling(window=3, min_periods=1).mean()

    fig2, ax2 = plt.subplots()
    ax2.plot(df_sorted["timestamp"], df_sorted["rolling_avg"], marker="o")
    ax2.set_title("Rolling Average Rating (window=3)")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Average Rating")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# --------------------------------------------------------------------------------
# 📝 Most Common Review Keywords
# --------------------------------------------------------------------------------

st.subheader("🔍 Most Common Keywords in Reviews")

def extract_keywords(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    words = text.split()
    stopwords = {"the", "is", "was", "and", "to", "it", "of", "in", "for", "very", "a", "an"}
    words = [w for w in words if w not in stopwords and len(w) > 3]
    return words

keywords = []
for review in df["review"]:
    keywords.extend(extract_keywords(review))

if len(keywords) > 0:
    keyword_counts = Counter(keywords).most_common(10)
    keyword_df = pd.DataFrame(keyword_counts, columns=["Keyword", "Frequency"])
    st.bar_chart(keyword_df.set_index("Keyword"))
else:
    st.info("Not enough data for keyword analysis.")

# --------------------------------------------------------------------------------
# 📆 Submissions Over Time
# --------------------------------------------------------------------------------

st.subheader("📆 Number of Submissions Over Time")

if "timestamp" in df:
    daily_counts = df.groupby(df["timestamp"].dt.date).size()

    fig3, ax3 = plt.subplots()
    ax3.plot(daily_counts.index, daily_counts.values, marker="o")
    ax3.set_title("Daily Submission Count")
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Submissions")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

st.success("Analytics updated successfully!")
