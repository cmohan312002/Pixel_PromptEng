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

# Generate questions for different rounds
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

def generate_round2():
    outputs = [
        "A system that organizes tasks and resources to optimize team productivity.",
        "A network of devices communicating wirelessly to monitor environments.",
        "A framework that predicts market trends using historical data.",
    ]
    forbidden_words = [
        ["project", "management", "tasks", "team", "productivity"],
        ["IoT", "devices", "wireless", "network", "sensors"],
        ["analytics", "market", "data", "trends", "predict"],
    ]
    index = random.randint(0, len(outputs) - 1)
    return outputs[index], forbidden_words[index]

def generate_round3():
    challenges = [
        "Generate a bedtime story about an astronaut exploring Mars.",
        "Write a poem about the ocean without mentioning water.",
        "Describe a futuristic city without using the word 'technology'.",
    ]
    forbidden_words = [
        ["astronaut", "space", "Mars", "rocket", "planet"],
        ["water", "ocean", "sea", "waves", "liquid"],
        ["technology", "future", "AI", "robot", "smart"],
    ]
    index = random.randint(0, len(challenges) - 1)
    return challenges[index], forbidden_words[index]

# Main game function
def main():
    st.title("🚀 Prompt Engineering Challenge")
    st.write(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    
    if "round" not in st.session_state:
        st.session_state.update({
            "round": 0, "player_name": "", "total_score": 0,
            "history": [], "question": "", "forbidden_words": [], "ai_output": ""
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
                st.session_state.history.append({"round": 1, "prompt": user_prompt})
                if st.button("Next Round"):
                    st.session_state.round = 2
                    st.session_state.ai_output, st.session_state.forbidden_words = generate_round2()

    elif st.session_state.round == 2:
        st.write(f"### Round 2 | Player: {st.session_state.player_name}")
        st.write(f"**AI Output:** {st.session_state.ai_output}")
        st.write(f"**Forbidden Words:** {', '.join(st.session_state.forbidden_words)}")
        user_prompt = st.text_area("Guess the prompt:")
        if st.button("Submit"):
            if not user_prompt.strip():
                st.error("Please enter a prompt before submitting.")
            elif contains_forbidden_words(user_prompt, st.session_state.forbidden_words):
                st.error("❌ You used a forbidden word. Try again!")
            else:
                st.session_state.history.append({"round": 2, "prompt": user_prompt})
                if st.button("Next Round"):
                    st.session_state.round = 3
                    st.session_state.question, st.session_state.forbidden_words = generate_round3()

    elif st.session_state.round == 3:
        st.write(f"### Round 3 | Player: {st.session_state.player_name}")
        st.write(f"**Challenge:** {st.session_state.question}")
        st.write(f"**Forbidden Words:** {', '.join(st.session_state.forbidden_words)}")
        user_prompt = st.text_area("Create your masterpiece:")
        if st.button("Submit"):
            if not user_prompt.strip():
                st.error("Please enter a prompt before submitting.")
            elif contains_forbidden_words(user_prompt, st.session_state.forbidden_words):
                st.error("❌ You used a forbidden word. Try again!")
            else:
                st.session_state.history.append({"round": 3, "prompt": user_prompt})
                st.session_state.round = 4

    elif st.session_state.round == 4:
        st.write("### Final Results")
        st.write("Game Over! Thanks for playing!")
        if st.button("Play Again"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.round = 0

if __name__ == "__main__":
    main()
