from fastapi import FastAPI,Query

app = FastAPI()

# Main endpoint
@app.get('/')

def Hi():
    return {"message": "Hello Pyhton"} #json format for the data


@app.get('/calculate_bmi')
def calculate_bmi(weight: float = Query(..., gt=20, lt= 150, description= "Weight in kg"),
                  height: float= Query(..., gt= 1.35, lt= 1.98, description= "Height in m")):
    
    
    bmi = weight / (height ** 2)
    
    if bmi < 18.5:
        message = 'You are underweight, eat more'
    elif 18.5 <= bmi < 25:
        message = 'You have normal weight'
    else:
        message = 'You are obesity'
    return {"your bmi: ": bmi,
            "Message": message}
# http://127.0.0.1:8000/calculate_bmi?weight=79&height=1.73

# run the api:
# uvicorn fastAPI_code:app --reload