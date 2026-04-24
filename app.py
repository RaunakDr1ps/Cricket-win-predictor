import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="T20 Win Probability", page_icon="🏏", layout="centered")

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #18202f 0%, #090b10 55%, #050608 100%);
}

.main-card {
    padding: 28px;
    border-radius: 22px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
}

.logo-card {
    text-align: center;
    padding: 18px;
    border-radius: 18px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    animation: float 3s ease-in-out infinite;
}

.team-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 86px;
    height: 86px;
    border-radius: 50%;
    background: linear-gradient(135deg, #ff4b4b, #ff944d);
    color: white;
    font-size: 26px;
    font-weight: 900;
    margin-bottom: 10px;
    box-shadow: 0 0 25px rgba(255, 75, 75, 0.35);
}

@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
    100% { transform: translateY(0px); }
}

div.stButton > button {
    background: linear-gradient(90deg, #ff4b4b, #ff944d);
    color: white;
    border-radius: 14px;
    height: 52px;
    font-size: 18px;
    font-weight: 700;
    border: none;
}

.result-box {
    padding: 18px;
    border-radius: 18px;
    background: rgba(0,255,140,0.12);
    border: 1px solid rgba(0,255,140,0.35);
}
</style>
""", unsafe_allow_html=True)

teams = [
    "Chennai Super Kings", "Mumbai Indians", "Royal Challengers Bangalore",
    "Kolkata Knight Riders", "Delhi Capitals", "Punjab Kings",
    "Rajasthan Royals", "Sunrisers Hyderabad", "Gujarat Titans",
    "Lucknow Super Giants"
]

team_badges = {
    "Chennai Super Kings": "CSK",
    "Mumbai Indians": "MI",
    "Royal Challengers Bangalore": "╭∩╮",
    "Kolkata Knight Riders": "KKR",
    "Delhi Capitals": "DC",
    "Punjab Kings": "PBKS",
    "Rajasthan Royals": "RR",
    "Sunrisers Hyderabad": "SRH",
    "Gujarat Titans": "GT",
    "Lucknow Super Giants": "LSG"
}

def win_probability(current_score, target, balls_left, wickets_left):
    runs_left = target - current_score
    balls_bowled = 120 - balls_left

    current_rr = (current_score / balls_bowled) * 6 if balls_bowled > 0 else 0
    required_rr = (runs_left / balls_left) * 6 if balls_left > 0 else 0

    if runs_left <= 0:
        return 1.0, current_rr, required_rr, runs_left

    if wickets_left <= 0:
        return 0.0, current_rr, required_rr, runs_left

    rr_gap = required_rr - current_rr

    wicket_factor = wickets_left / 10
    ball_factor = balls_left / 120

    pressure = 0

    if required_rr > 8:
        pressure += (required_rr - 8) * 0.12

    if required_rr > 12:
        pressure += (required_rr - 12) * 0.18

    if balls_left <= 30:
        pressure += 0.35

    if balls_left <= 12:
        pressure += 0.55

    if wickets_left <= 5:
        pressure += 0.25

    if wickets_left <= 3:
        pressure += 0.45

    base = 0.55
    score = base
    score += wicket_factor * 0.35
    score += ball_factor * 0.20
    score -= rr_gap * 0.08
    score -= pressure

    prob = 1 / (1 + math.exp(-4 * (score - 0.5)))

    return max(0.01, min(0.99, prob)), current_rr, required_rr, runs_left

st.markdown("""
<h1 style='text-align:center; font-size:52px;'>🏏 T20 Win Probability Engine</h1>
<p style='text-align:center; color:#b5b5b5; font-size:18px;'>
Real-time match pressure estimator • Built for cricket chase scenarios • Don't Bet
</p>
""", unsafe_allow_html=True)

batting_team = st.selectbox("Batting Team", teams)
bowling_team = st.selectbox("Bowling Team", teams)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="logo-card">
        <div class="team-logo">{team_badges[batting_team]}</div>
        <p>Batting Team</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="logo-card">
        <div class="team-logo">{team_badges[bowling_team]}</div>
        <p>Bowling Team</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Match Inputs")

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
        prob, current_rr, required_rr, runs_left = win_probability(
            current_score, target, balls_left, wickets_left
        )

        batting_prob = round(prob * 100, 2)
        bowling_prob = round((1 - prob) * 100, 2)

        st.markdown(f"""
        <div class="result-box">
            <h2>{batting_team}: {batting_prob}%</h2>
            <h3>{bowling_team}: {bowling_prob}%</h3>
        </div>
        """, unsafe_allow_html=True)

        st.progress(int(batting_prob))

        st.markdown("### Match Situation")
        st.write(f"Runs Left: {runs_left}")
        st.write(f"Balls Left: {balls_left}")
        st.write(f"Wickets Left: {wickets_left}")
        st.write(f"Current Run Rate: {round(current_rr, 2)}")
        st.write(f"Required Run Rate: {round(required_rr, 2)}")

        st.markdown("### Win Probability Momentum Graph 📈")
        graph_data = []

        for b in range(balls_left, 0, -3):
            temp_prob, _, _, _ = win_probability(
                current_score,
                target,
                b,
                wickets_left
            )

            graph_data.append({
                "Balls Left": b,
                f"{batting_team} Win %": temp_prob * 100
            })

        chart_df = pd.DataFrame(graph_data).set_index("Balls Left")
        st.line_chart(chart_df)
