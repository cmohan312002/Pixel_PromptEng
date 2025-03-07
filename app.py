import streamlit as st
import google.generativeai as genai
import random
from datetime import datetime
import re

# Access the API key from Streamlit secrets
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API key is missing. Please check your Streamlit secrets.")
    st.stop()
genai.configure(api_key=api_key)

# Enhanced AI response generation with error handling
def generate_ai_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Improved prompt evaluation and scoring system
def evaluate_prompt(question, user_prompt, ai_response):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        eval_prompt = (
            f"Evaluate how well the given user prompt aligns with the provided question. "
            f"Assign a score out of 10 for each category: Relevance, Creativity, Clarity, and Efficiency. "
            f"Provide a total score out of 40 and concise feedback.\n\n"
            f"**Question:** {question}\n"
            f"**User Prompt:** {user_prompt}\n"
            f"**AI Response:** {ai_response}\n\n"
            f"### Evaluation Criteria:\n"
            f"- **Relevance (X/10)**: How well does the prompt address the question?\n"
            f"- **Creativity (Y/10)**: How unique and effective is the prompt?\n"
            f"- **Clarity (Z/10)**: How well-structured and understandable is the prompt?\n"
            f"- **Efficiency (W/10)**: Does the prompt get a meaningful response concisely?\n"
            f"\nProvide the final score in this format:\n"
            f"- Relevance: X/10\n- Creativity: Y/10\n- Clarity: Z/10\n- Efficiency: W/10\n- **Total Score: (X+Y+Z+W)/40**\n"
            f"- Feedback: <Concise improvement points>"
        )
        eval_response = model.generate_content(eval_prompt).text
        
        # Extract scores using regex
        scores = re.findall(r"(\d+)/10", eval_response)
        if len(scores) >= 4:
            relevance, creativity, clarity, efficiency = map(int, scores[:4])
            total_score = relevance + creativity + clarity + efficiency
        else:
            return 5, 5, 5, 5, 20, "Default score due to parsing issue."
        
        # Extract feedback
        feedback_match = re.search(r"Feedback:\s*(.*)", eval_response)
        feedback = feedback_match.group(1) if feedback_match else "No feedback provided."
        
        return relevance, creativity, clarity, efficiency, total_score, feedback
    except Exception as e:
        return 5, 5, 5, 5, 20, f"Error evaluating: {str(e)}"

# Main app function
def main():
    st.title("🚀 Prompt Engineering Challenge - College Edition")
    st.write(f"Date: {datetime.now().strftime('%B %d, %Y')}")

    if "round" not in st.session_state:
        st.session_state.round = 1
        st.session_state.question = "Describe how a computer works."
    
    st.write(f"### Question: {st.session_state.question}")
    user_prompt = st.text_area("Craft your prompt:", height=100)
    
    if st.button("Submit"):
        if not user_prompt.strip():
            st.error("Please enter a prompt before submitting.")
        else:
            ai_response = generate_ai_response(user_prompt)
            relevance, creativity, clarity, efficiency, total_score, feedback = evaluate_prompt(
                st.session_state.question, user_prompt, ai_response
            )
            
            st.write(f"**AI Response:** {ai_response}")
            st.write(f"### Scoring Breakdown:")
            st.write(f"- **Relevance:** {relevance}/10")
            st.write(f"- **Creativity:** {creativity}/10")
            st.write(f"- **Clarity:** {clarity}/10")
            st.write(f"- **Efficiency:** {efficiency}/10")
            st.write(f"- **Total Score:** {total_score}/40")
            st.write(f"### Feedback:")
            st.write(feedback)

if __name__ == "__main__":
    main()
