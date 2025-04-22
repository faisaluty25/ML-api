from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from generate_workout_plan import generate_custom_plan

app = FastAPI()

# Load the model and encoders
recommender_model = joblib.load("recommendation_model.joblib")
label_encoders = joblib.load("label_encoders.joblib")
feature_names = ['Age', 'Gender', 'BMI', 'Duration Per Day', 'Workout Intensity']

# --- CALORIES CALCULATION ENDPOINT ---
class CaloriesInput(BaseModel):
    Age: int
    Gender: str
    Height_cm: float
    Weight_kg: float
    Heart_Rate: float
    Workout_Duration_mins: int
    Workout_Days: int
    Workout_Type: str

@app.post("/calculate-calories")
def calculate_calories(data: CaloriesInput):
    workout_factors = {
        "None": 0,
        "Yoga": 1,
        "Dancing": 2,
        "Cardio": 3,
        "HIIT": 4
    }
    workout_factor = workout_factors.get(data.Workout_Type, 0)
    calories_per_min = (data.Heart_Rate * data.Weight_kg * 0.0007) + (data.Age * 0.01) + workout_factor
    total_calories = calories_per_min * data.Workout_Duration_mins
    bmi = data.Weight_kg / ((data.Height_cm / 100) ** 2)

    return {
        "Total_Calories": round(total_calories, 2),
        "Calories_Per_Minute": round(calories_per_min, 2),
        "BMI": round(bmi, 2)
    }

# --- WORKOUT RECOMMENDER ENDPOINT ---
class WorkoutRecommendationInput(BaseModel):
    Age: int
    Gender: str
    BMI: float
    Duration_Per_Day: float
    Workout_Intensity: str
    Workout_Days: int 

@app.post("/recommend-workout")
def recommend_workout(input_data: WorkoutRecommendationInput):
    try:
        # Encode categorical values
        gender_encoded = label_encoders['Gender'].transform([input_data.Gender])[0]
        intensity_encoded = label_encoders['Workout Intensity'].transform([input_data.Workout_Intensity])[0]

        # Construct feature vector (including the missing Workout Days)
        features = [
            input_data.Age,
            gender_encoded,
            intensity_encoded,
            input_data.Workout_Days,  # Add Workout Days here
            input_data.BMI,
            input_data.Duration_Per_Day
        ]

        prediction = recommender_model.predict([features])[0]

        # Decode the prediction if it's encoded
        category_decoder = {0: 'High Effort', 1: 'Endurance', 2: 'Flexibility'}
        predicted_category = category_decoder.get(prediction, str(prediction))

        return {"Recommended_Workout_Category": predicted_category}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Encoding Error: {str(ve)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")



# --- CUSTOM WORKOUT PLAN ENDPOINT ---
class PlanInput(BaseModel):
    workout_days: int
    mode: str  # "full_body", "muscle", or "body_part"
    preferences: list[str]

@app.post("/generate-plan")
def generate_plan(data: PlanInput):
    plan = generate_custom_plan(
        workout_days=data.workout_days,
        mode=data.mode,
        preferences=data.preferences
    )
    return plan
