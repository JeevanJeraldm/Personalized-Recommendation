# Personalized Recommendation System using Ollama

AI-powered personalized learning recommendation system using Python, Streamlit, Ollama, and Llama 3.2.

## Features
- User profile and interests
- Skill level and preferred learning type
- Learning goal
- Five personalized recommendations
- Match scores and explanations
- Feedback-based recommendation updates
- Local LLM through Ollama

## Run
Install dependencies:
    pip install -r requirements.txt

Make sure Llama 3.2 is available:
    ollama pull llama3.2

Start the application:
    streamlit run app.py

Open http://localhost:8501

## Example
Interests: Artificial Intelligence, Python, Data Science
Level: Beginner
Preferred Type: Practical
Goal: Learn Artificial Intelligence through practical courses.

## Structure
PersonalizedRecommendation/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
