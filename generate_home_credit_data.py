import pandas as pd
import numpy as np
import random

def generate_synthetic_data(num_samples=5000):
    np.random.seed(42)
    random.seed(42)

    data = {
        'AMT_INCOME_TOTAL': [],
        'DAYS_EMPLOYED': [],
        'NAME_INCOME_TYPE': [],
        'CNT_CHILDREN': [],
        'FLAG_OWN_CAR': [],
        'FLAG_OWN_REALTY': [],
        'TARGET': [] # 0 (Repaid) or 1 (Default)
    }

    income_types = ['Working', 'Commercial associate', 'State servant', 'Pensioner', 'Student']
    
    for _ in range(num_samples):
        # Features
        inc_type = np.random.choice(income_types, p=[0.5, 0.2, 0.1, 0.15, 0.05])
        
        income = 0
        if inc_type == 'Working':
            income = np.random.randint(100000, 500000) # Annual income in INR (Simulated)
        elif inc_type == 'Commercial associate':
            income = np.random.randint(200000, 1000000)
        elif inc_type == 'State servant':
            income = np.random.randint(150000, 600000)
        elif inc_type == 'Student':
            income = np.random.randint(0, 100000)
        else: # Pensioner
            income = np.random.randint(50000, 300000)

        # Days Employed: Usually negative in Home Credit data (days since hire). 
        # We will generate "Years" positive then convert to negative days for realism or keep positive for simplicity of this script
        # Let's keep it negative to match Home Credit style if we were strict, but for training this fresh model, 
        # let's just use Positive Years for simplicity in mapping to the Form.
        # WAIT, user asked for DAYS_EMPLOYED. Let's stick to Home Credit convention: Negative values.
        # But form will ask "Years". We will convert in app.py. Here we generate consistent data.
        # 0 to 40 years. 
        years_employed = np.random.randint(0, 40)
        if inc_type == 'Pensioner' or inc_type == 'Student':
             years_employed = 0
             if inc_type == 'Pensioner': years_employed = 365243 # Magic number in Home Credit for pensioners
        
        days_employed = -1 * years_employed * 365
        if years_employed == 365243: days_employed = 365243

        children = np.random.choice([0, 1, 2, 3], p=[0.5, 0.3, 0.15, 0.05])
        own_car = np.random.choice(['Y', 'N'], p=[0.3, 0.7])
        own_realty = np.random.choice(['Y', 'N'], p=[0.6, 0.4])

        # Logic for target (probabilistic)
        score = 0
        if income > 300000: score += 20
        if inc_type in ['State servant', 'Commercial associate']: score += 15
        if days_employed < -1000: score += 10 # More than 3 years
        if days_employed < -3000: score += 10 # More than 8 years
        
        if own_car == 'Y': score += 10
        if own_realty == 'Y': score += 10
        if children == 0: score += 5 
        
        # Random noise
        score += np.random.randint(-15, 15)

        # Target 0 = Repaid, 1 = Default
        # Higher score = Better credit = 0
        target = 0 if score > 50 else 1
        
        data['AMT_INCOME_TOTAL'].append(income)
        data['DAYS_EMPLOYED'].append(days_employed)
        data['NAME_INCOME_TYPE'].append(inc_type)
        data['CNT_CHILDREN'].append(children)
        data['FLAG_OWN_CAR'].append(own_car)
        data['FLAG_OWN_REALTY'].append(own_realty)
        data['TARGET'].append(target)

    df = pd.DataFrame(data)
    df.to_csv('credit_data.csv', index=False)
    print("Synthetic Home Credit data generated: credit_data.csv")

if __name__ == "__main__":
    generate_synthetic_data()
