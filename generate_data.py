import pandas as pd
import numpy as np
import random

def generate_synthetic_data(num_samples=5000):
    np.random.seed(42)
    random.seed(42)

    data = {
        'Monthly_Income': [],
        'Employment_Type': [],
        'Smartphone_Ownership': [],
        'Avg_Recharge_Amount': [],
        'Bill_Payment_Behavior': [],
        'UPI_Txn_Frequency': [],
        'Location_Stability': [],
        'Prev_Loan_Repayment': [],
        'Loan_Repaid': [] # Target
    }

    employment_types = ['Daily wage', 'Self-employed', 'Salaried']
    payment_behaviors = ['Always on time', 'Sometimes late', 'Often late']
    upi_freqs = ['Low', 'Medium', 'High']

    for _ in range(num_samples):
        # Features
        emp_type = np.random.choice(employment_types, p=[0.4, 0.4, 0.2])
        
        income = 0
        if emp_type == 'Daily wage':
            income = np.random.randint(3000, 15000)
        elif emp_type == 'Self-employed':
            income = np.random.randint(10000, 50000)
        else:
            income = np.random.randint(15000, 80000)

        smartphone = np.random.choice(['Yes', 'No'], p=[0.8, 0.2])
        recharge = np.random.randint(100, 1000) if smartphone == 'Yes' else np.random.randint(50, 300)
        
        bill_behavior = np.random.choice(payment_behaviors, p=[0.5, 0.3, 0.2])
        upi_freq = np.random.choice(upi_freqs, p=[0.3, 0.4, 0.3])
        location_stable = np.random.choice(['Yes', 'No'], p=[0.7, 0.3])
        prev_loan = np.random.choice(['Yes', 'No'], p=[0.4, 0.6]) # Has history?

        # Logic for target (probabilistic)
        score = 0
        if income > 20000: score += 20
        if emp_type == 'Salaried': score += 15
        elif emp_type == 'Self-employed': score += 10
        
        if bill_behavior == 'Always on time': score += 25
        elif bill_behavior == 'Sometimes late': score += 10
        
        if upi_freq == 'High': score += 15
        elif upi_freq == 'Medium': score += 10
        
        if location_stable == 'Yes': score += 10
        if prev_loan == 'Yes': score += 15
        
        # Random noise
        score += np.random.randint(-15, 15)

        # Threshold for repayment (1) vs default (0)
        # Higher score = more likely to repay
        repaid = 1 if score > 50 else 0
        
        data['Monthly_Income'].append(income)
        data['Employment_Type'].append(emp_type)
        data['Smartphone_Ownership'].append(smartphone)
        data['Avg_Recharge_Amount'].append(recharge)
        data['Bill_Payment_Behavior'].append(bill_behavior)
        data['UPI_Txn_Frequency'].append(upi_freq)
        data['Location_Stability'].append(location_stable)
        data['Prev_Loan_Repayment'].append(prev_loan)
        data['Loan_Repaid'].append(repaid)

    df = pd.DataFrame(data)
    df.to_csv('credit_data.csv', index=False)
    print("Synthetic data generated: credit_data.csv")

if __name__ == "__main__":
    generate_synthetic_data()
