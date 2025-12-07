def recommended_actions_prompt(review, rating):
    return f"""
You are an expert customer service strategist.

Analyze the following customer review and rating.
Provide clear, actionable steps that an admin should take.

Rating: {rating}
Review: "{review}"

Respond in the following format:

1. Key Issue Identified:
2. Recommended Actions (3-5 bullet points):
3. Priority Level (High/Medium/Low):
4. Expected Outcome:

Make the actions realistic and business-focused.
"""
