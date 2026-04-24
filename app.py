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

team_logos = {
    "Chennai Super Kings": "data:image/png;base64,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",
    "Mumbai Indians": "https://upload.wikimedia.org/wikipedia/en/5/5c/Mumbai_Indians_Logo.svg",
    "Royal Challengers Bangalore": "https://upload.wikimedia.org/wikipedia/en/4/4f/Royal_Challengers_Bangalore_Logo.svg",
    "Kolkata Knight Riders": "https://upload.wikimedia.org/wikipedia/en/4/4c/Kolkata_Knight_Riders_Logo.svg",
    "Delhi Capitals": "https://upload.wikimedia.org/wikipedia/en/2/2f/Delhi_Capitals.svg",
    "Punjab Kings": "https://upload.wikimedia.org/wikipedia/en/d/d4/Punjab_Kings_Logo.svg",
    "Rajasthan Royals": "https://upload.wikimedia.org/wikipedia/en/6/60/Rajasthan_Royals_Logo.svg",
    "Sunrisers Hyderabad": "https://upload.wikimedia.org/wikipedia/en/8/81/Sunrisers_Hyderabad.svg",
    "Gujarat Titans": "https://upload.wikimedia.org/wikipedia/en/0/09/Gujarat_Titans_Logo.svg",
    "Lucknow Super Giants": "https://upload.wikimedia.org/wikipedia/en/2/23/Lucknow_Super_Giants_IPL_Logo.svg"
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
    <img src="{team_logos[batting_team]}" width="80">
    <p>Batting Team</p>
</div>
""", unsafe_allow_html=True)

with col2:
   st.markdown(f"""
<div class="logo-card">
    <img src="{team_logos[bowling_team]}" width="80">
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
