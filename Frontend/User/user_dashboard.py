import streamlit as st
import requests

BACKEND_URL = "https://ai-feedback-system-47yp.onrender.com/submit"

st.set_page_config(page_title="User Feedback", layout="centered")

st.title("✨ User Feedback Submission")

rating = st.slider("Rate your experience:", 1, 5, 5)
review = st.text_area("Write your review:")

if st.button("Submit"):
    if not review.strip():
        st.error("Please enter a review.")
    else:
        payload = {"rating": rating, "review": review}
        try:
            res = requests.post(BACKEND_URL, json=payload)
            if res.status_code == 200:
                st.success("Feedback submitted successfully!")
                st.subheader("AI Response:")
                st.write(res.json()["ai_response"])
            else:
                st.error("Error: Backend returned an error.")
        except Exception as e:
            st.error("Cannot connect to backend.")
            st.exception(e)
