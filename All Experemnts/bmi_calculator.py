def calculate_bmi():
    weight = float(input('your weight: '))
    height = float(input('your height: '))
    bmi = weight / (height ** 2)
    
    if bmi < 18.5:
        message = 'You are underweight, eat more'
    elif 18.5 <= bmi < 25:
        message = 'You have normal weight'
    else:
        message = 'You are obesity'
        
        print("Your BMI:", bmi)
        print(message)
        
calculate_bmi()