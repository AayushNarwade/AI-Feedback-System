import os
import uuid
import json
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
from storage import load_data, save_data
from prompts import (
    user_response_prompt,
    summary_prompt,
    recommended_actions_prompt
)

# -----------------
# INIT
# -----------------
app = Flask(__name__)
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"


# -----------------
# LLM CALL FUNCTION
# -----------------
def call_llm(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    response = requests.post(GROQ_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]


# -----------------
# ROUTES
# -----------------

@app.route("/")
def home():
    return {"message": "Fynd AI Feedback System API is running."}


# -----------------
# SUBMISSION (POST)
# -----------------
@app.route("/submit", methods=["POST"])
def submit_review():
    data = request.json
    rating = data.get("rating")
    review = data.get("review")

    if not rating or not review:
        return jsonify({"error": "Rating and review are required"}), 400

    # ------------------
    # LLM PROCESSING
    # ------------------
    ai_response = call_llm(user_response_prompt(review, rating))
    ai_summary = call_llm(summary_prompt(review))
    ai_actions = call_llm(recommended_actions_prompt(review, rating))

    # ------------------
    # SAVE DATA
    # ------------------
    submission = {
        "id": str(uuid.uuid4()),
        "rating": rating,
        "review": review,
        "ai_response": ai_response,
        "ai_summary": ai_summary,
        "ai_actions": ai_actions,
        "timestamp": datetime.utcnow().isoformat()
    }

    all_data = load_data()
    all_data.append(submission)
    save_data(all_data)

    return jsonify({
        "message": "Submission processed",
        "ai_response": ai_response
    })


# -----------------
# GET ALL SUBMISSIONS
# -----------------
@app.route("/submissions", methods=["GET"])
def get_submissions():
    return jsonify(load_data())


# -----------------
# ANALYTICS
# -----------------
@app.route("/analytics", methods=["GET"])
def analytics():
    data = load_data()

    if not data:
        return jsonify({"error": "No data found"})

    avg_rating = sum([d["rating"] for d in data]) / len(data)

    return jsonify({
        "total_submissions": len(data),
        "avg_rating": avg_rating,
    })


# -----------------
# RUN
# -----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
