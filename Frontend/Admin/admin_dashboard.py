import streamlit as st
import requests
import pandas as pd

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

# Analytics
try:
    analytics = requests.get(BACKEND_URL + "/analytics").json()
    st.subheader("📊 Analytics")
    if "total_submissions" in analytics:
        st.metric("Total Submissions", analytics["total_submissions"])
        st.metric("Average Rating", round(analytics["avg_rating"], 2))
    else:
        st.warning("Analytics unavailable")
except:
    st.error("Error loading analytics.")
