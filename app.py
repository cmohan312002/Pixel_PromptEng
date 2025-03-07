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

# AI response generation with error handling
def generate_ai_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Normalize scores to ensure consistency
def normalize_scores(scores):
    for key in scores:
        scores[key] = max(1, min(10, scores[key]))  # Keeping scores between 1 and 10
    return scores

# Weighted scoring system
def weighted_score(scores):
    weights = {"accuracy": 0.4, "creativity": 0.3, "clarity": 0.3}
    total = sum(scores[k] * weights[k] for k in scores)
    return round(total, 2)

# Check if prompt contains forbidden words
def contains_forbidden_words(prompt, forbidden_words):
    return any(word.lower() in prompt.lower() for word in forbidden_words)

# AI-driven scoring for relevance
def check_relevance(question, response):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        relevance_prompt = (
            f"Evaluate the following prompt based on relevance, creativity, and clarity.\n"
            f"- Relevance: Does it directly relate to the question? (1-10)\n"
            f"- Creativity: How unique is the approach? (1-10)\n"
            f"- Clarity: Is the phrasing clear? (1-10)\n"
            f"\nQuestion: {question}\nUser Prompt: {response}\n"
            f"Provide scores and a short justification."
        )
        relevance_response = model.generate_content(relevance_prompt).text
        scores = {"accuracy": 5, "creativity": 5, "clarity": 5}  # Default scores
        score_matches = re.findall(r"(\w+):\s*(\d+)" , relevance_response)
        for category, score in score_matches:
            if category.lower() in scores:
                scores[category.lower()] = int(score)
        return normalize_scores(scores)
    except Exception as e:
        st.warning(f"Error checking relevance: {str(e)}. Using default scores.")
        return {"accuracy": 5, "creativity": 5, "clarity": 5}

# Score a prompt
def score_prompt(prompt, ai_response, forbidden_words, question):
    if not prompt.strip():
        return 0, {"accuracy": 0, "creativity": 0, "clarity": 0}
    
    scores = check_relevance(question, ai_response)
    total = weighted_score(scores)
    return total, scores

# Round question generators
def generate_round1():
    questions = [
        "Explain what photosynthesis is.",
        "Describe how a computer works.",
        "What is the significance of the Eiffel Tower?",
    ]
    forbidden_words = [
        ["photosynthesis", "plants", "sunlight"],
        ["computer", "hardware", "software"],
        ["Eiffel Tower", "Paris", "France"],
    ]
    index = random.randint(0, len(questions) - 1)
    return questions[index], forbidden_words[index]

# Main game function
def main():
    st.title("🚀 Prompt Engineering Challenge")
    st.write(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    
    if "round" not in st.session_state:
        st.session_state.update({
            "round": 0, "player_name": "", "total_score": 0,
            "history": [], "question": "", "forbidden_words": []
        })
    
    if st.session_state.round == 0:
        player_name = st.text_input("Enter your name to start:")
        if player_name and st.button("Start Game"):
            st.session_state.player_name = player_name
            st.session_state.round = 1
            st.session_state.question, st.session_state.forbidden_words = generate_round1()

    elif st.session_state.round == 1:
        st.write(f"### Round 1 | Player: {st.session_state.player_name}")
        st.write(f"**Question:** {st.session_state.question}")
        st.write(f"**Forbidden Words:** {', '.join(st.session_state.forbidden_words)}")
        user_prompt = st.text_area("Craft your prompt:")
        if st.button("Submit"):
            if not user_prompt.strip():
                st.error("Please enter a prompt before submitting.")
            elif contains_forbidden_words(user_prompt, st.session_state.forbidden_words):
                st.error("❌ You used a forbidden word. Try again!")
            else:
                ai_response = generate_ai_response(user_prompt)
                st.write(f"**AI Response:** {ai_response}")
                score, breakdown = score_prompt(user_prompt, ai_response, st.session_state.forbidden_words, st.session_state.question)
                st.session_state.history.append({
                    "question": st.session_state.question, "prompt": user_prompt,
                    "response": ai_response, "score": score, "breakdown": breakdown
                })
                st.write(f"**Score:** {score}/10")
                st.session_state.total_score += score
                if st.button("Finish Game"):
                    st.session_state.round = 2

    elif st.session_state.round == 2:
        st.write("### Final Results")
        st.write(f"**Total Score:** {st.session_state.total_score}/10")
        sorted_history = sorted(st.session_state.history, key=lambda x: x['score'], reverse=True)
        st.write("### Top Prompts")
        for entry in sorted_history[:3]:
            st.write(f"**Prompt:** {entry['prompt']}")
            st.write(f"**Score:** {entry['score']}/10")
            st.write("---")
        if st.button("Play Again"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.round = 0

if __name__ == "__main__":
    main()
