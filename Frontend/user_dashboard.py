import streamlit as st
import requests

BACKEND_URL = "http://localhost:8080/submit"

st.title("✨ User Feedback Submission")

rating = st.slider("Rate your experience", 1, 5, 5)
review = st.text_area("Write your review")

if st.button("Submit"):
    payload = {"rating": rating, "review": review}
    res = requests.post(BACKEND_URL, json=payload)

    if res.status_code == 200:
        st.success("Submitted successfully!")
        st.write("### AI Response:")
        st.write(res.json()["ai_response"])
    else:
        st.error("Error submitting your feedback.")

#https://<your-render-backend-url>/submit