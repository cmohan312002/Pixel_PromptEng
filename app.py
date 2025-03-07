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

# Generate AI response with error handling
def generate_ai_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Check for forbidden words
def contains_forbidden_words(prompt, forbidden_words):
    return any(word.lower() in prompt.lower() for word in forbidden_words)

# Score calculation based on question and input
def score_prompt(prompt, ai_response, forbidden_words, round_type, question):
    if not prompt.strip():
        return 0, {"accuracy": 0, "creativity": 0, "clarity": 0, "efficiency": 0, "rule_compliance": 0}
    
    try:
        accuracy = 10 - (sum(1 for word in forbidden_words if word.lower() in prompt.lower()))
        accuracy = max(0, accuracy)  # Ensure score doesn't go negative
        
        scores = {
            "accuracy": accuracy,
            "creativity": min(10, len(set(prompt.split())) // 2),
            "clarity": min(10, 10 - abs(15 - len(prompt.split())) // 2),
            "efficiency": min(10, 10 - len(prompt.split()) // 5) if len(prompt.split()) > 0 else 0,
            "rule_compliance": 10 if not contains_forbidden_words(prompt, forbidden_words) else 0
        }
        
        total_score = sum(scores.values())
        return total_score, scores
    except Exception as e:
        st.error(f"Error calculating score: {str(e)}")
        return 0, {"accuracy": 0, "creativity": 0, "clarity": 0, "efficiency": 0, "rule_compliance": 0}

# Round generators
def generate_round1():
    questions = [
        "Explain what photosynthesis is.",
        "Describe how a computer works.",
        "What is the significance of the Eiffel Tower?",
        "Explain the concept of gravity.",
        "Describe the process of making coffee."
    ]
    forbidden_words_lists = [
        ["photosynthesis", "plants", "sunlight", "energy", "chlorophyll"],
        ["computer", "hardware", "software", "CPU", "memory"],
        ["Eiffel Tower", "Paris", "landmark", "France", "iron"],
        ["gravity", "force", "Earth", "mass", "Newton"],
        ["coffee", "beans", "brew", "grind", "caffeine"]
    ]
    index = random.randint(0, len(questions) - 1)
    return questions[index], forbidden_words_lists[index]

def generate_round2():
    outputs = [
        "A system that organizes tasks and resources to optimize team productivity.",
        "A network of devices communicating wirelessly to monitor environments.",
        "A framework that predicts market trends using historical data.",
        "A process that ensures software meets user needs through iterative testing.",
        "A strategy that aligns team goals with organizational objectives."
    ]
    forbidden_words_lists = [
        ["project", "management", "tasks", "team", "productivity"],
        ["IoT", "devices", "wireless", "network", "sensors"],
        ["analytics", "market", "data", "trends", "predict"],
        ["software", "testing", "user", "bugs", "iteration"],
        ["strategy", "goals", "team", "organization", "plan"]
    ]
    index = random.randint(0, len(outputs) - 1)
    return outputs[index], forbidden_words_lists[index]

def generate_round3():
    challenges = [
        "Generate a bedtime story about an astronaut exploring Mars.",
        "Write a poem about the ocean without mentioning water.",
        "Describe a futuristic city without using the word 'technology'.",
        "Explain how a tree grows without using the word 'photosynthesis'.",
        "Tell a story about a dragon and a knight without using the word 'fire'."
    ]
    forbidden_words_lists = [
        ["astronaut", "space", "Mars", "rocket", "planet"],
        ["water", "ocean", "sea", "waves", "liquid"],
        ["technology", "future", "AI", "robot", "smart"],
        ["photosynthesis", "sunlight", "chlorophyll", "energy", "plants"],
        ["fire", "flame", "burn", "heat", "dragon"]
    ]
    index = random.randint(0, len(challenges) - 1)
    return challenges[index], forbidden_words_lists[index]

# Main app
def main():
    st.title("🚀 Prompt Engineering Challenge")
    st.write(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    
    if "round" not in st.session_state:
        st.session_state.round = 0
        st.session_state.player_name = ""
        st.session_state.total_score = 0

    if st.session_state.round == 0:
        player_name = st.text_input("Enter your name:")
        if player_name and st.button("Start Game"):
            st.session_state.player_name = player_name
            st.session_state.round = 1
            st.session_state.question, st.session_state.forbidden_words = generate_round1()

    elif st.session_state.round == 1:
        st.write(f"**Round 1: Forbidden Words Challenge | Player: {st.session_state.player_name}**")
        st.write(f"**Question:** {st.session_state.question}")
        st.write(f"**Forbidden Words:** {', '.join(st.session_state.forbidden_words)}")
        user_prompt = st.text_area("Craft your prompt:")
        if st.button("Submit"):
            ai_response = generate_ai_response(user_prompt)
            score, breakdown = score_prompt(user_prompt, ai_response, st.session_state.forbidden_words, "round1", st.session_state.question)
            st.session_state.total_score += score
            st.write(f"**Score:** {score}/50")
            st.write(f"**Breakdown:** {breakdown}")
            if st.button("Next Round"):
                st.session_state.round = 2
                st.session_state.ai_output, st.session_state.forbidden_words = generate_round2()
    
if __name__ == "__main__":
    main()
