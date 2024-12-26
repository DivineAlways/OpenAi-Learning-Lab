import streamlit as st
import random
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="OpenAI Learning Lab",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and interactive elements
st.markdown("""
<style>
.main {
    background-color: #1E1E1E;
    color: #E0E0E0;
}
.challenge-card {
    background-color: #2D2D2D;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #404040;
    margin: 10px 0;
}
.success-text {
    color: #4CAF50;
}
.hint-text {
    color: #FFB74D;
}
.score-text {
    color: #2196F3;
    font-size: 24px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'completed_challenges' not in st.session_state:
    st.session_state.completed_challenges = set()

# Learning content
CHALLENGES = {
    "beginner": [
        {
            "title": "ChatGPT Basics",
            "description": "Create a simple chat completion request",
            "hint": "Use openai.chat.completions.create with gpt-3.5-turbo",
            "code_template": """
import openai

response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Say hello!"}
    ]
)
            """,
            "points": 10
        },
        {
            "title": "DALL·E Image Generation",
            "description": "Generate an image using DALL·E",
            "hint": "Use openai.images.generate with a descriptive prompt",
            "code_template": """
response = openai.images.generate(
    model="dall-e-3",
    prompt="A cute robot learning to code",
    n=1
)
            """,
            "points": 15
        }
    ],
    "intermediate": [
        {
            "title": "Function Calling",
            "description": "Implement a weather checking function",
            "hint": "Define a function schema and use it in chat completion",
            "code_template": """
functions = [{
    "name": "get_weather",
    "description": "Get weather in location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string"},
            "unit": {"type": "string"}
        }
    }
}]
            """,
            "points": 20
        }
    ],
    "expert": [
        {
            "title": "Fine-tuning",
            "description": "Set up a model fine-tuning job",
            "hint": "Prepare training data and create a fine-tuning job",
            "code_template": """
training_file = openai.files.create(
    file=open("training.jsonl", "rb"),
    purpose="fine-tune"
)
job = openai.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-3.5-turbo"
)
            """,
            "points": 30
        }
    ]
}

# Sidebar
st.sidebar.title("Learning Progress")
st.sidebar.markdown(f"**Score:** {st.session_state.score}")
st.sidebar.markdown(f"**Challenges Completed:** {len(st.session_state.completed_challenges)}")

# Main content
st.title("🧪 OpenAI Learning Lab")
st.markdown("Learn OpenAI features through interactive challenges!")

# Level selection
level = st.selectbox("Choose your level:", ["beginner", "intermediate", "expert"])

# Display challenges for selected level
st.markdown(f"## {level.title()} Challenges")

for idx, challenge in enumerate(CHALLENGES[level]):
    with st.expander(f"Challenge {idx + 1}: {challenge['title']}"):
        st.markdown(f"**Description:** {challenge['description']}")
        st.markdown(f"**Points:** {challenge['points']}")
        
        # Show hint button
        if st.button(f"Show Hint {idx}", key=f"hint_{idx}"):
            st.markdown(f"💡 **Hint:** {challenge['hint']}")
        
        # Code editor
        user_code = st.text_area("Your Code:", challenge['code_template'], key=f"code_{idx}")
        
        # Submit button
        if st.button(f"Submit Solution {idx}", key=f"submit_{idx}"):
            if challenge['title'] not in st.session_state.completed_challenges:
                st.session_state.score += challenge['points']
                st.session_state.completed_challenges.add(challenge['title'])
                st.markdown(f"✨ **Success!** You earned {challenge['points']} points!")
                st.balloons()
            else:
                st.markdown("You've already completed this challenge!")

# Practice playground
st.markdown("## 🎮 Practice Playground")
playground_code = st.text_area(
    "Experiment with OpenAI APIs here:",
    "# Try out your own code here!\n\nimport openai\n\n"
)

if st.button("Run Code"):
    st.code(playground_code)
    st.markdown("⚠️ Note: This is a simulation. In a real app, this would execute your code.")

# Learning resources
st.markdown("## 📚 Additional Resources")
resources = [
    {"title": "OpenAI Documentation", "url": "https://platform.openai.com/docs"},
    {"title": "API Reference", "url": "https://platform.openai.com/docs/api-reference"},
    {"title": "Examples", "url": "https://platform.openai.com/examples"}
]

for resource in resources:
    st.markdown(f"- [{resource['title']}]({resource['url']})")

# Save progress
if st.button("Save Progress"):
    progress = {
        "score": st.session_state.score,
        "completed_challenges": list(st.session_state.completed_challenges),
        "timestamp": datetime.now().isoformat()
    }
    st.download_button(
        "Download Progress",
        data=json.dumps(progress, indent=2),
        file_name="openai_learning_progress.json",
        mime="application/json"
    )