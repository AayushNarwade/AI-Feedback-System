def user_response_prompt(review, rating):
    return f"""
You are a helpful AI assistant replying to a customer review.

User rating: {rating} stars  
User review: "{review}"

Write a short, friendly, human-like response.  
Do NOT mention you are an AI.  
Keep it under 40 words.
"""


def summary_prompt(review):
    return f"""
Summarize the following customer review in one sentence:

Review: "{review}"

Output only the summary.
"""


def recommended_actions_prompt(review, rating):
    return f"""
You are an analytics assistant.

Based on the review below, suggest **2–3 recommended actions** the company should take.

Rating: {rating}
Review: "{review}"

Output in bullet points.
"""
