import streamlit as st
import math

teams = [
    "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Delhi Capitals", "Punjab Kings",
    "Rajasthan Royals", "Sunrisers Hyderabad", "Gujarat Titans",
    "Lucknow Super Giants"
]

st.set_page_config(page_title="IPL Win Predictor", page_icon="🏏")

st.title("🏏 IPL Win Predictor")
st.write("Estimate batting team's win probability during a chase. Don't Bet")

batting_team = st.selectbox("Batting Team", teams)
bowling_team = st.selectbox("Bowling Team", teams)

current_score = st.number_input("Current Score", min_value=0, step=1)
target = st.number_input("Target", min_value=1, step=1)
balls_left = st.number_input("Balls Left", min_value=1, max_value=120, step=1)
wickets_left = st.number_input("Wickets Left", min_value=0, max_value=10, step=1)

if st.button("Predict Win Probability"):
    if batting_team == bowling_team:
        st.error("Batting and bowling team cannot be same.")
    elif current_score >= target:
        st.success(f"{batting_team} Win Probability: 100%")
    elif wickets_left == 0:
        st.error(f"{batting_team} Win Probability: 0%")
    else:
        runs_left = target - current_score
        balls_bowled = 120 - balls_left

        current_rr = (current_score / balls_bowled) * 6 if balls_bowled > 0 else 0
        required_rr = (runs_left / balls_left) * 6

        pressure = required_rr - current_rr

        score = 1.2 - (0.55 * pressure) + (0.22 * (wickets_left - 5)) + (0.008 * (balls_left - 60))
        prob = 1 / (1 + math.exp(-score))

        prob = max(0, min(1, prob))

        st.success(f"{batting_team} Win Probability: {round(prob * 100, 2)}%")
        st.info(f"{bowling_team} Win Probability: {round((1 - prob) * 100, 2)}%")

        st.write("### Match Situation")
        st.write(f"Runs Left: {runs_left}")
        st.write(f"Balls Left: {balls_left}")
        st.write(f"Wickets Left: {wickets_left}")
        st.write(f"Current Run Rate: {round(current_rr, 2)}")
        st.write(f"Required Run Rate: {round(required_rr, 2)}")
