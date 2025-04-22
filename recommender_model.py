import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
import os

# Create 'model' directory if it doesn't exist
os.makedirs("model", exist_ok=True)

# Load dataset
df = pd.read_csv("workout_fitness_tracker_data.csv")

# Select relevant columns
df = df[[  
    'Age', 'Gender', 'Height (cm)', 'Weight (kg)', 
    'Workout Duration (mins)', 'Workout Intensity', 'Workout Type'
]]

# Add synthetic feature
np.random.seed(42)
df['Workout Days'] = np.random.choice([2, 3, 4, 5, 6], size=len(df))

# Add BMI and Duration Per Day
df['Height (m)'] = df['Height (cm)'] / 100
df['BMI'] = df['Weight (kg)'] / (df['Height (m)'] ** 2)
df['Duration Per Day'] = df['Workout Duration (mins)'] / df['Workout Days']

# Drop unneeded columns
df.drop(columns=['Height (cm)', 'Weight (kg)', 'Height (m)', 'Workout Duration (mins)'], inplace=True)

# Map workout type to categories
df['Workout Type'] = LabelEncoder().fit_transform(df['Workout Type'])
workout_type_decoder = {0: 'Cardio', 1: 'Cycling', 2: 'HIIT', 3: 'Running', 4: 'Strength', 5: 'Yoga'}
df['Workout Type'] = df['Workout Type'].map(workout_type_decoder)

merge_map = {
    'HIIT': 'High Effort',
    'Strength': 'High Effort',
    'Cardio': 'Endurance',
    'Running': 'Endurance',
    'Cycling': 'Endurance',
    'Yoga': 'Flexibility'
}
df['Workout Category'] = df['Workout Type'].map(merge_map)

# Encode categorical columns
label_encoders = {}
for col in ['Gender', 'Workout Intensity', 'Workout Category']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Prepare features and target
X = df.drop(columns=['Workout Type', 'Workout Category'])
y = df['Workout Category']

# Train the model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model (optional)
y_pred = rf_model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("✅ F1 Score:", f1_score(y_test, y_pred, average='weighted'))
print("✅ Classification Report:\n", classification_report(y_test, y_pred))

# Save model and encoders
joblib.dump(rf_model, "model/recommendation_model.joblib")
joblib.dump(label_encoders, "model/label_encoders.joblib")
print("✅ Model and encoders saved to /model folder.")

