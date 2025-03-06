import streamlit as st
import google.generativeai as genai
import random
from datetime import datetime

# Access the API key from Streamlit secrets
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Enhanced AI response generation with error handling
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

# Improved scoring system
def score_prompt(prompt, ai_response, forbidden_words, round_type):
    scores = {
        "accuracy": min(10, 5 + len(ai_response.split()) // 10),
        "creativity": min(10, len(set(prompt.split())) // 2),
        "clarity": min(10, 10 - abs(15 - len(prompt.split())) // 2),
        "efficiency": min(10, 10 - len(prompt.split()) // 5) if len(prompt.split()) > 0 else 0,
        "rule_compliance": 10 if not contains_forbidden_words(prompt, forbidden_words) else 0
    }
    if round_type == "round1":
        scores["creativity"] = min(10, scores["creativity"] + 2)
    elif round_type == "round2":
        scores["accuracy"] = min(10, scores["accuracy"] + 2)
    elif round_type == "round3":
        scores["clarity"] = min(10, scores["clarity"] + 2)
    total_score = sum(scores.values())
    return total_score, scores

# Round generators (Round 1 and Round 3 restored to original)
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
    st.title("🚀 Prompt Engineering Challenge - College Edition")
    st.write(f"Date: {datetime.now().strftime('%B %d, %Y')} | For MCA & MMS Students")

    # Initialize session state
    if "round" not in st.session_state:
        st.session_state.round = 0
        st.session_state.player_name = ""
        st.session_state.round_scores = []
        st.session_state.total_score = 0
        st.session_state.history = []
        st.session_state.question = ""
        st.session_state.forbidden_words = []
        st.session_state.ai_output = ""
        st.session_state.show_next_round_button = False
        st.session_state.submitted_round3 = False

    # Round 0: Get player name and start
    if st.session_state.round == 0:
        st.write("Welcome to the challenge! Please enter your name to begin.")
        player_name = st.text_input("Your Name:")
        if player_name and st.button("Start Game"):
            st.session_state.player_name = player_name
            st.session_state.round = 1
            st.session_state.question, st.session_state.forbidden_words = generate_round1()

    # Round 1
    elif st.session_state.round == 1:
        st.write(f"### Round 1: Forbidden Words Challenge | Player: {st.session_state.player_name}")
        st.write(f"**Question:** {st.session_state.question}")
        st.write(f"**Forbidden Words:** {', '.join(st.session_state.forbidden_words)}")
        user_prompt = st.text_area("Craft your prompt:", height=100)
        if st.button("Submit"):
            if contains_forbidden_words(user_prompt, st.session_state.forbidden_words):
                st.error("❌ Oops! You used a forbidden word. Try again!")
            else:
                ai_response = generate_ai_response(user_prompt)
                st.write(f"**AI Response:** {ai_response}")
                score, breakdown = score_prompt(user_prompt, ai_response, st.session_state.forbidden_words, "round1")
                st.session_state.round_scores.append(("Round 1", score))
                st.session_state.total_score += score
                st.session_state.history.append({
                    "round": "Round 1",
                    "question": st.session_state.question,  # Store the question
                    "prompt": user_prompt,
                    "response": ai_response,
                    "score": score,
                    "breakdown": breakdown
                })
                st.write(f"**Score:** {score}/50")
                st.write(f"**Breakdown:** {breakdown}")
                st.session_state.show_next_round_button = True

        if st.session_state.show_next_round_button and st.button("Next Round"):
            st.session_state.round = 2
            st.session_state.show_next_round_button = False
            st.session_state.ai_output, st.session_state.forbidden_words = generate_round2()

    # Round 2
    elif st.session_state.round == 2:
        st.write(f"### Round 2: Reverse Engineer the Prompt | Player: {st.session_state.player_name}")
        st.write(f"**AI Output:** {st.session_state.ai_output}")
        st.write(f"**Forbidden Words:** {', '.join(st.session_state.forbidden_words)}")
        user_prompt = st.text_area("Guess the prompt:", height=100)
        if st.button("Submit"):
            if contains_forbidden_words(user_prompt, st.session_state.forbidden_words):
                st.error("❌ Oops! You used a forbidden word. Try again!")
            else:
                ai_response = generate_ai_response(user_prompt)
                st.write(f"**AI Response:** {ai_response}")
                score, breakdown = score_prompt(user_prompt, ai_response, st.session_state.forbidden_words, "round2")
                st.session_state.round_scores.append(("Round 2", score))
                st.session_state.total_score += score
                st.session_state.history.append({
                    "round": "Round 2",
                    "question": st.session_state.ai_output,  # Store the AI output as the "question"
                    "prompt": user_prompt,
                    "response": ai_response,
                    "score": score,
                    "breakdown": breakdown
                })
                st.write(f"**Score:** {score}/50")
                st.write(f"**Breakdown:** {breakdown}")
                st.session_state.show_next_round_button = True

        if st.session_state.show_next_round_button and st.button("Next Round"):
            st.session_state.round = 3
            st.session_state.show_next_round_button = False
            st.session_state.question, st.session_state.forbidden_words = generate_round3()

    # Round 3
    elif st.session_state.round == 3:
        st.write(f"### Round 3: Creative Prompt Master | Player: {st.session_state.player_name}")
        st.write(f"**Challenge:** {st.session_state.question}")
        st.write(f"**Forbidden Words:** {', '.join(st.session_state.forbidden_words)}")
        user_prompt = st.text_area("Create your masterpiece:", height=100)
        if st.button("Submit"):
            if contains_forbidden_words(user_prompt, st.session_state.forbidden_words):
                st.error("❌ Oops! You used a forbidden word. Try again!")
            else:
                ai_response = generate_ai_response(user_prompt)
                st.write(f"**AI Response:** {ai_response}")
                score, breakdown = score_prompt(user_prompt, ai_response, st.session_state.forbidden_words, "round3")
                st.session_state.round_scores.append(("Round 3", score))
                st.session_state.total_score += score
                st.session_state.history.append({
                    "round": "Round 3",
                    "question": st.session_state.question,  # Store the challenge
                    "prompt": user_prompt,
                    "response": ai_response,
                    "score": score,
                    "breakdown": breakdown
                })
                st.write(f"**Score:** {score}/50")
                st.write(f"**Breakdown:** {breakdown}")
                st.session_state.submitted_round3 = True

        if st.session_state.submitted_round3 and st.button("Finish Game"):
            st.session_state.round = 4
            st.session_state.submitted_round3 = False

    # Round 4: Final Results
    elif st.session_state.round == 4:
        st.write(f"### Final Results | Player: {st.session_state.player_name}")
        st.write("🎉 Congratulations on completing the challenge!")
        for round_name, round_score in st.session_state.round_scores:
            st.write(f"{round_name}: {round_score}/50")
        st.write(f"**Total Score:** {st.session_state.total_score}/150")
        if st.button("Review Previous Rounds"):
            st.session_state.round = 5
        if st.button("Play Again"):
            st.session_state.round = 0
            st.session_state.player_name = ""
            st.session_state.round_scores = []
            st.session_state.total_score = 0
            st.session_state.history = []
            st.session_state.show_next_round_button = False

    # Round 5: Review Mode with Questions
    elif st.session_state.round == 5:
        st.write(f"### Review Your Game | Player: {st.session_state.player_name}")
        for entry in st.session_state.history:
            st.write(f"#### {entry['round']}")
            # Display the question/output appropriately based on the round
            if entry['round'] == "Round 2":
                st.write(f"**AI Output:** {entry['question']}")
            else:
                st.write(f"**Question/Challenge:** {entry['question']}")
            st.write(f"**Your Prompt:** {entry['prompt']}")
            st.write(f"**AI Response:** {entry['response']}")
            st.write(f"**Score:** {entry['score']}/50")
            st.write(f"**Breakdown:** {entry['breakdown']}")
            st.write("---")
        if st.button("Back to Results"):
            st.session_state.round = 4
        if st.button("Play Again"):
            st.session_state.round = 0
            st.session_state.player_name = ""
            st.session_state.round_scores = []
            st.session_state.total_score = 0
            st.session_state.history = []
            st.session_state.show_next_round_button = False

if __name__ == "__main__":
    main()
