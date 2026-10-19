




import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(
    page_title="AI Quiz Generator",
    page_icon="🧠"
)

st.title("🧠 AI Quiz Generator")
st.write("Create quizzes instantly with Gemini AI!")

api_key = os.getenv("GEMINI_API_KEY")

topic = st.text_input(
    "Enter your quiz topic",
    placeholder="e.g. Python, Science, AI"
)

difficulty = st.selectbox(
    "Select difficulty",
    ["Easy", "Medium", "Hard"]
)

num_questions = st.selectbox(
    "Number of questions",
    [5, 10, 15]
)

if st.button("Generate Quiz", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    elif not api_key:
        st.error("GEMINI_API_KEY is missing. Check your .env file.")
    else:
        prompt = f"""
Create {num_questions} multiple-choice quiz questions
about {topic} at {difficulty} difficulty.

For each question, provide:
- The question
- Four options labelled A, B, C, D
- The correct answer
- A short explanation

Keep the questions accurate and number them clearly.
"""

        try:
            with st.spinner("Gemini is creating your quiz..."):
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.subheader("Your Quiz")
            st.markdown(response.text)

            st.download_button(
                "Download Quiz",
                data=response.text,
                file_name="my_quiz.txt",
                mime="text/plain"
            )

        except Exception as error:
            st.error("Quiz generate nahi hua. Error details:")
            st.code(str(error))
