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
    font-size: 42px;
    font-weight: 900;
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
    "Royal Challengers Bangalore": "data:image/jpeg;base64,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",
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

    pressure = required_rr - current_rr
    score = 1.2 - (0.55 * pressure) + (0.22 * (wickets_left - 5)) + (0.008 * (balls_left - 60))
    prob = 1 / (1 + math.exp(-score))
    return max(0, min(1, prob)), current_rr, required_rr, runs_left

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
        for b in range(max(1, balls_left - 30), min(120, balls_left + 31)):
            temp_prob, _, _, _ = win_probability(current_score, target, b, wickets_left)
            graph_data.append({
                "Balls Left": b,
                f"{batting_team} Win %": temp_prob * 100
            })

        chart_df = pd.DataFrame(graph_data).set_index("Balls Left")
        st.line_chart(chart_df)
