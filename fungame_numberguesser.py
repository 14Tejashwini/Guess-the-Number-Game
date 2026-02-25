import streamlit as st
import random
import time

st.set_page_config(page_title="🎯 Guess The Number", page_icon="🎯", layout="centered")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    h1 {
        text-align: center;
        color: #facc15;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Guess The Number")

# Sidebar - Difficulty Level
st.sidebar.header("⚙️ Game Settings")
difficulty = st.sidebar.selectbox(
    "Choose Difficulty",
    ["Easy (1-50)", "Medium (1-100)", "Hard (1-500)"]
)

if difficulty == "Easy (1-50)":
    max_number = 50
elif difficulty == "Medium (1-100)":
    max_number = 100
else:
    max_number = 500

# Initialize session state
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, max_number)
    st.session_state.attempts = 0
    st.session_state.history = []

# Restart Game Button
if st.sidebar.button("🔄 Restart Game"):
    st.session_state.secret_number = random.randint(1, max_number)
    st.session_state.attempts = 0
    st.session_state.history = []
    st.success("Game Restarted!")

st.markdown(f"### 🔢 Guess a number between 1 and {max_number}")

col1, col2 = st.columns([3,1])

with col1:
    guess = st.number_input("Enter your guess", min_value=1, max_value=max_number, step=1)

with col2:
    submit = st.button("🚀 Submit")

# Feedback phrases
def get_feedback(secret, guess):
    diff = abs(secret - guess)

    if diff == 0:
        return "correct"
    elif diff <= 3:
        return random.choice([
            "🔥 BOILING HOT!",
            "😱 So close you can taste it!",
            "💥 You're right there!",
            "🔥🔥 It's burning!"
        ])
    elif diff <= 10:
        return random.choice([
            "🌡️ Very warm!",
            "😉 You're getting closer!",
            "🙂 Not far now!",
        ])
    elif diff <= 20:
        return random.choice([
            "🌤️ Warm!",
            "🤔 You're in the zone!",
        ])
    else:
        return random.choice([
            "❄️ Ice cold!",
            "🥶 Way off!",
            "🌊 Freezing!"
        ])

if submit:
    st.session_state.attempts += 1
    st.session_state.history.append(guess)

    feedback = get_feedback(st.session_state.secret_number, guess)

    # Animated progress bar (fake suspense)
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.005)
        progress.progress(i + 1)

    if feedback == "correct":
        st.balloons()
        st.success(f"🎉 CORRECT! You guessed it in {st.session_state.attempts} attempts!")
    else:
        if guess < st.session_state.secret_number:
            st.info(f"{feedback} 📉 Try higher!")
        else:
            st.info(f"{feedback} 📈 Try lower!")

# Attempt Counter
st.markdown(f"### 🏆 Attempts: {st.session_state.attempts}")

# Show Guess History
if st.session_state.history:
    with st.expander("📜 Guess History"):
        st.write(st.session_state.history)

# Fun Achievement System
if st.session_state.attempts == 1 and st.session_state.history:
    if st.session_state.history[-1] == st.session_state.secret_number:
        st.success("👑 LEGEND! First try!")

elif 1 < st.session_state.attempts <= 5 and st.session_state.history:
    if st.session_state.history[-1] == st.session_state.secret_number:
        st.success("🌟 Sharp Shooter!")

elif st.session_state.attempts > 10 and st.session_state.history:
    if st.session_state.history[-1] == st.session_state.secret_number:
        st.warning("😅 That took a while, but you got it!")

st.markdown("---")
st.caption("Website by TR")