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

# Check relevance of response to question/output
def check_relevance(question, response):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        relevance_prompt = (
                f"Evaluate the following user-generated prompt based on its alignment with the given question, "
                f"the creativity of the approach, clarity in phrasing, and efficiency in eliciting a relevant and insightful response. "
                f"Each evaluation should be based on the following criteria:\n\n"
                
                f"- **Relevance**: Does the user’s prompt address the core of the question and provide clear direction for generating a meaningful response?\n"
                f"- **Creativity**: How innovative or unique is the user’s approach to framing the prompt? Does it introduce new angles or perspectives?\n"
                f"- **Clarity**: Is the prompt easy to understand and interpret? Are the instructions clear and concise?\n"
                
                f"Each round will evaluate the quality of the prompt in these categories, and a score should be assigned from 1 to 10 for each.\n\n"
                
                f"Round 1: Evaluate the user prompt based on basic structure and clarity.\n"
                f"Round 2: Assess creativity and originality in how the prompt engages with the question.\n"
                f"Round 3: Evaluate the overall impact of the prompt in driving the best, most insightful response.\n\n"
                
                f"Here’s how to structure your evaluation:\n"
                f"- **Relevance**: X/10\n"
                f"- **Creativity**: Y/10\n"
                f"- **Clarity**: Z/10\n"
                
                f"Example:\n\n"
                f"Question: {question}\n"
                f"User Prompt: {response}\n\n"
                f"Feedback: Provide concise feedback explaining the scores and suggestions for improvement."
            )
        relevance_response = model.generate_content(relevance_prompt).text
        # Extract the numeric score using regex
        score_match = re.search(r"Score:\s*(\d+)", relevance_response)
        if score_match:
            score = int(score_match.group(1))
            return min(10, max(0, score))
        else:
            return 5  # Default if parsing fails
    except Exception as e:
        st.warning(f"Error checking relevance: {str(e)}. Defaulting to 5.")
        return 5

# Check for forbidden words (case-insensitive)
def contains_forbidden_words(prompt, forbidden_words):
    return any(word.lower() in prompt.lower() for word in forbidden_words)

# Updated scoring system with improved logic
def score_prompt(prompt, ai_response, forbidden_words, round_type, question):
    if not prompt.strip():
        return 0, {"accuracy": 0, "creativity": 0, "clarity": 0}

    try:
        # Ensure AI-generated accuracy score is within a reasonable range
        accuracy = check_relevance(question, ai_response)
        accuracy = max(1, min(10, accuracy))  # Keep accuracy within 1-10 range

        # Creativity score based on unique words and sentence complexity
        unique_words = len(set(prompt.split()))
        total_words = len(prompt.split())
        creativity = min(10, max(1, unique_words / max(1, total_words) * 10))

        # Clarity score based on balanced length (not too short, not too long)
        ideal_length = 15  # Ideal prompt length in words
        clarity = max(1, min(10, 10 - abs(ideal_length - total_words) // 2))

        # Round-specific adjustments
        if round_type == "round1":
            creativity = min(10, creativity + 2)
        elif round_type == "round2":
            accuracy = min(10, accuracy + 2)
        elif round_type == "round3":
            clarity = min(10, clarity + 2)

        scores = {"accuracy": round(accuracy), "creativity": round(creativity), "clarity": round(clarity)}
        total_score = sum(scores.values())

        return total_score, scores
    except Exception as e:
        st.error(f"Error calculating score: {str(e)}")
        return 0, {"accuracy": 0, "creativity": 0, "clarity": 0}

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

if __name__ == "__main__":
    main()
