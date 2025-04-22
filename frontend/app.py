import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# API base URL
API_BASE = "http://127.0.0.1:8000"

# Page config
st.set_page_config(
    page_title="Fitness Vision",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #1E1E1E 0%, #2C3E50 100%);
            color: #FFFFFF;
            font-family: 'Inter', sans-serif;
        }
        .main-header {
            text-align: center;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            margin-bottom: 2rem;
        }
        .stCard {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        .stButton>button {
            background: linear-gradient(45deg, #FF4B4B, #4A90E2);
            color: white;
            border-radius: 50px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("<div class='main-header'><h1>💪 Fitness Vision</h1><p>Your personalized workout and calorie companion</p></div>", unsafe_allow_html=True)

# Navigation
page = st.sidebar.radio("Choose a page:", ["🏋️ Calories Calculator", "🏋️ Workout Recommendation", "🏋️ Custom Workout Plan"])

# --- 1. Calories Calculator ---
if page == "🏋️ Calories Calculator":
    st.subheader("🔥 Calories Burned Calculator")
    with st.form("calorie_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 10, 80, 25)
            gender = st.selectbox("Gender", ["Male", "Female"])
            height = st.number_input("Height (cm)", 100, 250, 170)
            weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
        with col2:
            heart_rate = st.number_input("Heart Rate", 60, 200, 100)
            workout_duration = st.slider("Workout Duration (mins)", 10, 120, 30)
            workout_days = st.slider("Workout Days per Week", 1, 7, 3)
            workout_type = st.selectbox("Workout Type", ["None", "Yoga", "Dancing", "Cardio", "HIIT"])

        submitted = st.form_submit_button("Calculate Calories")
        if submitted:
            payload = {
                "Age": age,
                "Gender": gender,
                "Height_cm": height,
                "Weight_kg": weight,
                "Heart_Rate": heart_rate,
                "Workout_Duration_mins": workout_duration,
                "Workout_Days": workout_days,
                "Workout_Type": workout_type
            }
            res = requests.post(f"{API_BASE}/calculate-calories", json=payload)
            if res.status_code == 200:
                result = res.json()
                st.success("✅ Calculation Complete!")
                st.metric("Total Calories Burned", f"{result['Total_Calories']} kcal")
                st.metric("Calories per Minute", f"{result['Calories_Per_Minute']} kcal/min")
                st.metric("BMI", result["BMI"])
            else:
                st.error("Failed to calculate. Please check your inputs.")

# --- 2. Workout Recommendation ---
elif page == "🏋️ Workout Recommendation":
    st.subheader("🤖 AI-Powered Workout Recommendation")
    with st.form("recommendation_form"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", 10, 80, 25, key="rec_age")
            gender = st.selectbox("Gender", ["Male", "Female"], key="rec_gender")
            bmi = st.number_input("BMI", 10.0, 40.0, 22.5)
        with col2:
            duration_per_day = st.slider("Workout Duration Per Day (mins)", 10, 120, 30)
            workout_intensity = st.selectbox("Workout Intensity", ["Low", "Medium", "High"])
            workout_days = st.slider("Workout Days per Week", 1, 7, 3)

        submitted = st.form_submit_button("Get Recommendation")
        if submitted:
            payload = {
                "Age": age,
                "Gender": gender,
                "BMI": bmi,
                "Duration_Per_Day": duration_per_day,
                "Workout_Intensity": workout_intensity,
                "Workout_Days": workout_days
            }
            res = requests.post(f"{API_BASE}/recommend-workout", json=payload)
            if res.status_code == 200:
                category = res.json()["Recommended_Workout_Category"]
                st.success(f"🎯 Recommended Workout Category: **{category}**")
            else:
                st.error(res.json()["detail"])

# --- 3. Custom Workout Plan ---
elif page == "🏋️ Custom Workout Plan":
    st.subheader("📋 Custom Weekly Workout Plan")
    with st.form("plan_form"):
        workout_days = st.slider("Workout Days per Week", 1, 7, 3)
        mode = st.selectbox("Plan Mode", ["full_body", "muscle", "body_part"])
        preferences = st.multiselect("Muscle or Body Part Preferences (optional)", [
            "chest", "back", "shoulders", "waist", "upper arms", "lower arms", 
            "upper legs", "lower legs", "cardio", "neck"
        ])

        submitted = st.form_submit_button("Generate Plan")
        if submitted:
            payload = {
                "workout_days": workout_days,
                "mode": mode,
                "preferences": preferences
            }
            res = requests.post(f"{API_BASE}/generate-plan", json=payload)
            if res.status_code == 200:
                response = res.json()

                title = response.get("title", "Your Custom Plan")
                st.success(f"💪 Here's your custom weekly workout plan: **{title}**")

                full_plan = response.get("days", {})
                for day, exercises in full_plan.items():
                    st.markdown(f"### 📅 {day}")
                    if not exercises:
                        st.markdown("- Rest day 💤")
                    else:
                        for ex in exercises:
                            st.markdown(
                                f"**{ex['name'].title()}**  \n"
                                f"• **Body Part:** {ex['bodyPart']}  \n"
                                f"• **Target:** {ex['target']}  \n"
                                f"• **Equipment:** {ex['equipment']}  \n"
                                f"![gif]({ex['gifUrl']})"
                            )
            else:
                st.error("❌ Failed to generate plan. Try again.")
