Here’s a complete **README.md** file for your GitHub repo, including sections like installation, usage, and contribution. You can tweak or expand this as needed for your project setup.

---

# 🚀 Prompt Engineering Challenge – College Edition 🎮

A fun, interactive **Streamlit web app** where students can test their **prompt engineering skills** through **three dynamic AI-powered rounds**. Designed for **tech fests**, **workshops**, or **learning events**, this game challenges players to craft prompts, reverse-engineer outputs, and creatively respond — all while scoring based on multiple metrics.

---

## 🌟 Features

- 🎯 **Three Engaging Rounds**:
  - **Round 1**: Forbidden Words Challenge – Craft prompts without using specific keywords.
  - **Round 2**: Reverse Engineer the Prompt – Guess the prompt based on an AI-generated output.
  - **Round 3**: Creative Challenge – Generate the most creative prompt to solve a unique challenge.
  
- 🤖 Powered by **Google Gemini API** for real-time AI responses.
- 📊 **Scoring System**:
  - Evaluates **accuracy**, **creativity**, **clarity**, **efficiency**, and **rule compliance**.
  - Uses AI to judge prompt relevance and award scores per round.
  
- 🔐 Secure API key handling using **Streamlit Secrets**.
- 🏆 Final results with detailed **score breakdown** and **review mode**.

---

## 🚀 Demo

Coming soon! (Add screenshots or a Streamlit Cloud link if hosted)

---

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cmohan312002/Pixel_PromptEng.git
   cd prompt-engineering-challenge
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Streamlit Secrets for Gemini API key**:
   - Create a `.streamlit/secrets.toml` file:
     ```toml
     GEMINI_API_KEY = "your-gemini-api-key-here"
     ```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
📦 prompt-engineering-challenge/
 ┣ 📜 app.py               # Main Streamlit app
 ┣ 📜 requirements.txt     # Required Python packages
 ┣ 📁 .streamlit/          # Streamlit secrets configuration
 ┃ ┗ 📜 secrets.toml
```

---

## 📊 Scoring Logic

| Metric            | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| Accuracy          | Relevance of AI response to the challenge question                         |
| Creativity        | Unique word usage in prompt                                                |
| Clarity           | Balanced length and coherence                                              |
| Efficiency        | Prompt length optimization                                                 |
| Rule Compliance   | Avoidance of forbidden words                                               |

---

## 🙌 Contributing

Contributions, suggestions, and feature requests are welcome!

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m 'Add new feature'`.
4. Push to branch: `git push origin feature-name`.
5. Open a pull request.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

Questions or feedback? Reach out via [email](mailto:cmohan312002@gmail.com) or open an [issue](https://github.com/cmohan312002/Pixel_PromptEng/issues).

---

Let me know if you’d like to include badges (e.g., Streamlit, Gemini AI, License), sample screenshots, or hosting instructions for Streamlit Cloud!
