import streamlit as st
import google.generativeai as genai
import random

# Configure Gemini API
genai.configure(api_key="")  # Replace with your Gemini API key

# List all available models
def list_available_models():
    models = genai.list_models()
    for model in models:
        print(model.name)

# Function to generate AI response using Gemini
def generate_ai_response(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Replace with the correct model name
    response = model.generate_content(prompt)
    return response.text

# Function to check if the prompt contains forbidden words
def contains_forbidden_words(prompt, forbidden_words):
    for word in forbidden_words:
        if word.lower() in prompt.lower():
            return True
    return False

# Function to score the user's prompt
def score_prompt(prompt, ai_response, forbidden_words, round_type):
    scores = {
        "accuracy": 0,
        "creativity": 0,
        "clarity": 0,
        "efficiency": 0,
        "rule_compliance": 0
    }

    # Rule Compliance
    scores["rule_compliance"] = 10 if not contains_forbidden_words(prompt, forbidden_words) else 0

    # Accuracy (placeholder logic)
    scores["accuracy"] = 10  # Replace with actual logic to compare prompt and AI response

    # Creativity (placeholder logic)
    scores["creativity"] = 8  # Replace with actual logic to evaluate creativity

    # Clarity (placeholder logic)
    scores["clarity"] = 9  # Replace with actual logic to evaluate clarity

    # Efficiency (placeholder logic)
    scores["efficiency"] = 7  # Replace with actual logic to evaluate efficiency

    # Adjust scoring based on round type
    if round_type == "round1":
        scores["creativity"] += 2  # Extra points for creativity in Round 1
    elif round_type == "round2":
        scores["accuracy"] += 2  # Extra points for accuracy in Round 2
    elif round_type == "round3":
        scores["clarity"] += 2  # Extra points for clarity in Round 3

    total_score = sum(scores.values())
    return total_score, scores

# Function to generate Round 1 question and forbidden words
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

# Function to generate Round 2 AI output and forbidden words
def generate_round2():
    outputs = [
        "A metallic creature that can assist humans with tasks, has sensors, and moves independently.",
        "A device that uses lenses to capture and store visual memories.",
        "A natural phenomenon where water falls from the sky in droplets.",
        "A structure that connects two land masses over a body of water.",
        "A process where plants convert sunlight into energy."
    ]
    forbidden_words_lists = [
        ["robot", "AI", "automation", "machine", "humanoid"],
        ["camera", "lens", "photo", "image", "capture"],
        ["rain", "water", "sky", "droplets", "weather"],
        ["bridge", "structure", "connect", "land", "water"],
        ["photosynthesis", "plants", "sunlight", "energy", "chlorophyll"]
    ]
    index = random.randint(0, len(outputs) - 1)
    return outputs[index], forbidden_words_lists[index]

# Function to generate Round 3 challenge and forbidden words
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

# Streamlit App
def main():
    st.title("Prompt Engineering Challenge")
    st.write("Welcome to the Prompt Engineering Challenge! Type 'Ready' to begin.")

    if "round" not in st.session_state:
        st.session_state.round = 0
        st.session_state.total_score = 0

    if st.session_state.round == 0:
        user_input = st.text_input("Type 'Ready' to begin:")
        if user_input.lower() == "ready":
            st.session_state.round = 1

    if st.session_state.round == 1:
        st.write("### Round 1: Forbidden Words Challenge")
        question, forbidden_words = generate_round1()
        st.write(f"**Question:** {question}")
        st.write(f"**Forbidden Words:** {', '.join(forbidden_words)}")
        user_prompt = st.text_input("Enter your prompt:")
        if user_prompt:
            if contains_forbidden_words(user_prompt, forbidden_words):
                st.error("❌ Invalid: You used a forbidden word! Try again.")
            else:
                ai_response = generate_ai_response(user_prompt)
                st.write(f"**AI Response:** {ai_response}")
                score, breakdown = score_prompt(user_prompt, ai_response, forbidden_words, "round1")
                st.session_state.total_score += score
                st.write(f"**Your Score:** {score}")
                st.write(f"**Score Breakdown:** {breakdown}")
                st.session_state.round = 2

    if st.session_state.round == 2:
        st.write("### Round 2: Guess the Prompt")
        output, forbidden_words = generate_round2()
        st.write(f"**AI Output:** {output}")
        st.write(f"**Forbidden Words:** {', '.join(forbidden_words)}")
        user_prompt = st.text_input("Guess the prompt:")
        if user_prompt:
            if contains_forbidden_words(user_prompt, forbidden_words):
                st.error("❌ Invalid: You used a forbidden word! Try again.")
            else:
                ai_response = generate_ai_response(user_prompt)
                st.write(f"**AI Response:** {ai_response}")
                score, breakdown = score_prompt(user_prompt, ai_response, forbidden_words, "round2")
                st.session_state.total_score += score
                st.write(f"**Your Score:** {score}")
                st.write(f"**Score Breakdown:** {breakdown}")
                st.session_state.round = 3

    if st.session_state.round == 3:
        st.write("### Round 3: Ultimate Prompt Hack")
        challenge, forbidden_words = generate_round3()
        st.write(f"**Challenge:** {challenge}")
        st.write(f"**Forbidden Words:** {', '.join(forbidden_words)}")
        user_prompt = st.text_input("Enter your prompt:")
        if user_prompt:
            if contains_forbidden_words(user_prompt, forbidden_words):
                st.error("❌ Invalid: You used a forbidden word! Try again.")
            else:
                ai_response = generate_ai_response(user_prompt)
                st.write(f"**AI Response:** {ai_response}")
                score, breakdown = score_prompt(user_prompt, ai_response, forbidden_words, "round3")
                st.session_state.total_score += score
                st.write(f"**Your Score:** {score}")
                st.write(f"**Score Breakdown:** {breakdown}")
                st.write(f"### 🎉 Total Score: {st.session_state.total_score}")
                st.session_state.round = 0  # Reset for a new game

# Run the app
if __name__ == "__main__":
    main()
