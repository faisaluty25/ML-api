import requests

API_HEADERS = {
    'x-rapidapi-key': "e90a745955mshaef134b6f28017ep1ed56bjsn7fd09b596b4c",
    'x-rapidapi-host': "exercisedb.p.rapidapi.com"
}

def get_exercises_by_target(muscle: str, limit: int = 3):
    url = f"https://exercisedb.p.rapidapi.com/exercises/target/{muscle.lower()}"
    try:
        res = requests.get(url, headers=API_HEADERS)
        if res.status_code == 200:
            return res.json()[:limit]
    except Exception:
        pass
    return []

def get_exercises_by_body_part(part: str, limit: int = 3):
    url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{part.lower()}"
    try:
        res = requests.get(url, headers=API_HEADERS)
        if res.status_code == 200:
            return res.json()[:limit]
    except Exception:
        pass
    return []

def get_full_body_exercises():
    groups = [
        ['chest', 'shoulders'],
        ['back', 'upper arms'],
        ['waist'],
        ['lower arms', 'neck'],
        ['upper legs', 'lower legs'],
        ['cardio']
    ]
    plan = []
    for grp in groups:
        exs = []
        for part in grp:
            items = get_exercises_by_body_part(part, limit=1)
            if items:
                exs.append(items[0])
        if exs:
            plan.append(exs)
    return plan

def generate_custom_plan(workout_days: int, mode: str, preferences: list):
    daily_plan = [[] for _ in range(workout_days)]
    title = ""

    if mode == "full_body":
        title = "🔥 Full‑Body Plan"
        groups = get_full_body_exercises()
        for i, grp in enumerate(groups):
            day = i % workout_days
            daily_plan[day].extend(grp)
    else:
        if mode == "muscle":
            title = "🏋️‍♂️ Muscle‑Based Plan"
            source = get_exercises_by_target
        else:
            title = "🏋️‍♂️ Body Part‑Based Plan"
            source = get_exercises_by_body_part

        for pref in preferences:
            exs = source(pref, limit=2)
            for i, ex in enumerate(exs):
                daily_plan[i % workout_days].append(ex)

    # Format into a readable dict
    return {
        "title": title,
        "days": {
            f"Day {i+1}": daily_plan[i] for i in range(workout_days)
        }
    }
