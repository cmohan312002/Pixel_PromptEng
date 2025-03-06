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

# Improved scoring system with detailed logic
def score_prompt(prompt, ai_response, forbidden_words, round_type):
    scores = {
        "accuracy": 0,
        "creativity": 0,
        "clarity": 0,
        "efficiency": 0,
        "rule_compliance": 0
    }

    # Rule Compliance (10 if no forbidden words, 0 if any are used)
    scores["rule_compliance"] = 10 if not contains_forbidden_words(prompt, forbidden_words) else 0

    # Accuracy (based on response relevance)
    scores["accuracy"] = min(10, 5 + len(ai_response.split()) // 10)  # Longer, relevant responses score higher

    # Creativity (based on prompt uniqueness)
    unique_words = len(set(prompt.split()))
    scores["creativity"] = min(10, unique_words // 2)  # Reward diverse vocabulary

    # Clarity (based on prompt length and readability)
    prompt_length = len(prompt.split())
    scores["clarity"] = min(10, 10 - abs(15 - prompt_length) // 2)  # Optimal length ~15 words

    # Efficiency (shorter prompts that get good responses score higher)
    scores["efficiency"] = min(10, 10 - prompt_length // 5) if prompt_length > 0 else 0

    # Round-specific bonuses
    if round_type == "round1":
        scores["creativity"] = min(10, scores["creativity"] + 2)
    elif round_type == "round2":
        scores["accuracy"] = min(10, scores["accuracy"] + 2)
    elif round_type == "round3":
        scores["clarity"] = min(10, scores["clarity"] + 2)

    total_score = sum(scores.values())
    return total_score, scores

# Round generators with more variety
def generate_round1():
    questions = [
        "Explain how stars shine in the night sky.",
        "Describe the journey of a raindrop from cloud to ground.",
        "What makes a rainbow appear after rain?",
        "Explain how a bicycle stays balanced while moving.",
        "Describe how honey is made by bees."
    ]
    forbidden_words_lists = [
        ["stars", "shine", "night", "light", "sky"],
        ["raindrop", "cloud", "ground", "water", "fall"],
        ["rainbow", "rain", "colors", "light", "spectrum"],
        ["bicycle", "balance", "wheels", "ride", "move"],
        ["honey", "bees", "hive", "nectar", "sweet"]
    ]
    index = random.randint(0, len(questions) - 1)
    return questions[index], forbidden_words_lists[index]

def generate_round2():
    outputs = [
        "A glowing orb that illuminates the darkness with ancient fusion energy.",
        "A winged machine that defies gravity and carries people across continents.",
        "A crystalline substance that falls from above and blankets the earth.",
        "A mechanical arm that assists in building towering structures.",
        "A living network that cleans the air we breathe."
    ]
    forbidden_words_lists = [
        ["sun", "light", "fusion", "energy", "star"],
        ["airplane", "fly", "wings", "travel", "sky"],
        ["snow", "cold", "flakes", "winter", "ice"],
        ["robot", "arm", "build", "construction", "machine"],
        ["trees", "air", "oxygen", "forest", "leaves"]
    ]
    index = random.randint(0, len(outputs) - 1)
    return outputs[index], forbidden_words_lists[index]

def generate_round3():
    challenges = [
        "Write a mystery story about a missing comet in space.",
        "Create a song about the wind without mentioning air.",
        "Describe a magical forest without using the word 'trees'.",
        "Explain how birds navigate long distances without saying 'fly'.",
        "Invent a tale of a time-traveling scholar without using 'time'."
    ]
    forbidden_words_lists = [
        ["comet", "space", "star", "orbit", "sky"],
        ["air", "wind", "blow", "breeze", "gust"],
        ["trees", "forest", "wood", "leaves", "branches"],
        ["fly", "birds", "wings", "sky", "feathers"],
        ["time", "travel", "past", "future", "clock"]
    ]
    index = random.randint(0, len(challenges) - 1)
    return challenges[index], forbidden_words_lists[index]

# Main app
def main():
    st.title("🚀 Prompt Engineering Challenge - Student Edition")
    st.write(f"Date: {datetime.now().strftime('%B %d, %Y')} | Test your skills and creativity!")

    # Initialize session state
    if "round" not in st.session_state:
        st.session_state.round = 0
        st.session_state.round_scores = []  # Track scores for each round
        st.session_state.total_score = 0
        st.session_state.question = ""
        st.session_state.forbidden_words = []
        st.session_state.ai_output = ""
        st.session_state.show_next_round_button = False

    # Round 0: Start screen
    if st.session_state.round == 0:
        st.write("Get ready to challenge your prompt engineering skills across 3 exciting rounds!")
        if st.button("Start Game"):
            st.session_state.round = 1
            st.session_state.question, st.session_state.forbidden_words = generate_round1()

    # Round 1
    elif st.session_state.round == 1:
        st.write("### Round 1: Forbidden Words Challenge")
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
                st.write(f"**Score:** {score}/50")
                st.write(f"**Breakdown:** {breakdown}")
                st.session_state.show_next_round_button = True
        if st.session_state.show_next_round_button and st.button("Next Round"):
            st.session_state.round = 2
            st.session_state.show_next_round_button = False
            st.session_state.ai_output, st.session_state.forbidden_words = generate_round2()

    # Round 2
    elif st.session_state.round == 2:
        st.write("### Round 2: Reverse Engineer the Prompt")
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
                st.write(f"**Score:** {score}/50")
                st.write(f"**Breakdown:** {breakdown}")
                st.session_state.show_next_round_button = True
        if st.session_state.show_next_round_button and st.button("Next Round"):
            st.session_state.round = 3
            st.session_state.show_next_round_button = False
            st.session_state.question, st.session_state.forbidden_words = generate_round3()

    # Round 3
    elif st.session_state.round == 3:
        st.write("### Round 3: Creative Prompt Master")
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
                st.write(f"**Score:** {score}/50")
                st.write(f"**Breakdown:** {breakdown}")
                st.write("### Final Results")
                for round_name, round_score in st.session_state.round_scores:
                    st.write(f"{round_name}: {round_score}/50")
                st.write(f"**Total Score:** {st.session_state.total_score}/150")
                st.session_state.show_next_round_button = True
        if st.session_state.show_next_round_button and st.button("Play Again"):
            st.session_state.round = 0
            st.session_state.round_scores = []
            st.session_state.total_score = 0
            st.session_state.show_next_round_button = False

if __name__ == "__main__":
    main()
