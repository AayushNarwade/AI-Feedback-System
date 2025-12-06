import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://localhost:8080"

st.title("🛠 Admin Dashboard")

# Load data
submissions = requests.get(BACKEND_URL + "/submissions").json()
df = pd.DataFrame(submissions)

st.subheader("📋 All Submissions")
st.dataframe(df)

# Analytics
analytics = requests.get(BACKEND_URL + "/analytics").json()

st.subheader("📊 Analytics")
st.write(f"Total submissions: {analytics['total_submissions']}")
st.write(f"Average rating: {analytics['avg_rating']:.2f}")
