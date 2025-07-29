import streamlit as st
import pandas as pd
from query_handler import aggregate_and_query
import random
import datetime

# Expanded trivia list
TRIVIA = [
    "Did you know? The first computer bug was a moth found in a Harvard Mark II computer in 1947.",
    "Python was named after Monty Python, not the snake!",
    "Did you know? The QWERTY keyboard layout was designed in the 1870s to prevent typewriter keys from jamming, not for typing efficiency.",
    "Did you know? The term 'spam' for unwanted emails comes from a 1970 Monty Python sketch about the canned meat.",
    "Did you know? The first email was sent by Ray Tomlinson in 1971, and it was something like 'QWERTYUIOP'.",
    "Did you know? The world's first website, created by Tim Berners-Lee in 1991, explained what the World Wide Web was.",
    "Did you know? Ada Lovelace wrote the first computer program in the 1840s for Charles Babbage's Analytical Engine.",
    "Did you know? The '@' symbol in email addresses was chosen because it meant 'at' in accounting ledgers.",
    "Did you know? The first computer mouse was invented in 1964 and was made of wood.",
    "Did you know? Wi-Fi doesn't stand for anything—it's a made-up term, not 'Wireless Fidelity'.",
    "Did you know? The first video game, Tennis for Two, was created in 1958 on an oscilloscope.",
    "Did you know? The hashtag symbol (#) was originally called an 'octothorpe' by Bell Labs engineers."
]

# Leaderboard (CSV storage)
LEADERBOARD_FILE = 'leaderboard.csv'

def load_leaderboard():
    try:
        return pd.read_csv(LEADERBOARD_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Query', 'Creativity Score'])

def save_leaderboard(df):
    df.to_csv(LEADERBOARD_FILE, index=False)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'badges' not in st.session_state:
    st.session_state.badges = []

st.title("Smart Knowledge Assistant Dashboard")

# Daily Challenge
today = datetime.date.today()
challenge = "Today's Challenge: Ask about a Python best practice from GitHub!"
st.subheader(challenge)

# Interactive Chat Input
prompt = st.chat_input("Ask a question about tech docs, wikis, or APIs:")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = aggregate_and_query(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response + " 😊"})
    
    # Gamification: Award points
    st.session_state.points += 10
    if st.session_state.points >= 50 and "Query Enthusiast" not in st.session_state.badges:
        st.session_state.badges.append("Query Enthusiast")
        st.success("Badge Unlocked: Query Enthusiast!")
    
    # Fun: Did You Know? (50% chance)
    if random.choice([True, False]):
        st.info(random.choice(TRIVIA))
    
    # Leaderboard Update
    creativity_score = len(prompt.split()) + random.randint(1, 10)
    df = load_leaderboard()
    new_entry = pd.DataFrame({'Query': [prompt], 'Creativity Score': [creativity_score]})
    df = pd.concat([df, new_entry]).sort_values('Creativity Score', ascending=False).head(10)
    save_leaderboard(df)

# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Sidebar for Points, Badges, and Leaderboard
with st.sidebar:
    st.header("Your Stats")
    st.write(f"Points: {st.session_state.points}")
    st.write("Badges:")
    for badge in st.session_state.badges:
        st.write(f"- {badge}")
    st.subheader("Query Leaderboard")
    st.table(load_leaderboard())

# Note: For internal docs, add file upload and parse (e.g., via PyPDF2), then include in context.
