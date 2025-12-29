import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect, url_for
import joblib
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)

MODEL_PATH = 'model.pkl'
ENCODER_PATH = 'encoders.pkl'
DB_PATH = 'credit.db'

if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODER_PATH)
    print("Model and encoders loaded successfully.")
else:
    print("Error: Model or encoders not found. Please run train_model.py first.")
    model = None
    encoders = None

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS credit_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amt_income_total REAL,
            days_employed REAL,
            name_income_type TEXT,
            cnt_children INTEGER,
            flag_own_car TEXT,
            flag_own_realty TEXT,
            predicted_default_probability REAL,
            credit_score INTEGER,
            risk_level TEXT,
            decision TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized.")

init_db()

def populate_db_from_csv():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT count(*) FROM credit_applications')
    count = c.fetchone()[0]
    
    if count > 0:
        conn.close()
        return

    print("Populating database from CSV...")
    try:
        if not os.path.exists('credit_data.csv'):
            print("credit_data.csv not found. Skipping import.")
            return

        df = pd.read_csv('credit_data.csv')
        
        X = df[['AMT_INCOME_TOTAL', 'DAYS_EMPLOYED', 'NAME_INCOME_TYPE', 'CNT_CHILDREN', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY']].copy()
        
        for col in ['NAME_INCOME_TYPE', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY']:
            le = encoders[col]
            X[col] = le.transform(X[col])
            
        probs = model.predict_proba(X)
        prob_defaults = probs[:, 1]
        
        rows_to_insert = []
        for i, row in df.iterrows():
            p_default = prob_defaults[i]
            score = int((1 - p_default) * 100)
            
            risk = "High"
            decision = "REJECT"
            if p_default < 0.15:
                risk = "Low"
                decision = "APPROVE"
            elif p_default <= 0.35:
                risk = "Medium"
                decision = "APPROVE (Conditional)"
                
            rows_to_insert.append((
                float(row['AMT_INCOME_TOTAL']),
                float(row['DAYS_EMPLOYED']),
                row['NAME_INCOME_TYPE'],
                int(row['CNT_CHILDREN']),
                row['FLAG_OWN_CAR'],
                row['FLAG_OWN_REALTY'],
                float(p_default),
                score,
                risk,
                decision
            ))
            
        c.executemany('''
            INSERT INTO credit_applications 
            (amt_income_total, days_employed, name_income_type, cnt_children, 
            flag_own_car, flag_own_realty, predicted_default_probability, 
            credit_score, risk_level, decision)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', rows_to_insert)
        
        conn.commit()
        print(f"Imported {len(rows_to_insert)} records from CSV.")
        
    except Exception as e:
        print("Error importing CSV:", e)
    finally:
        conn.close()

if model and encoders:
    populate_db_from_csv()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/assess')
def assess():
    return render_template('assess.html')

@app.route('/history')
def history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM credit_applications ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return render_template('history.html', applications=rows)

@app.route('/fairness')
def fairness():
    return render_template('fairness.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not encoders:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.json
        print("Received data:", data)

        income = float(data['income_total'])
        years_employed = float(data['years_employed'])
        days_employed = -1 * years_employed * 365
        income_type = data['income_type']
        children = int(data['cnt_children'])
        own_car = data['flag_own_car']
        own_realty = data['flag_own_realty']

        input_data = {
            'AMT_INCOME_TOTAL': [income],
            'DAYS_EMPLOYED': [days_employed],
            'NAME_INCOME_TYPE': [income_type],
            'CNT_CHILDREN': [children],
            'FLAG_OWN_CAR': [own_car],
            'FLAG_OWN_REALTY': [own_realty]
        }
        
        df_input = pd.DataFrame(input_data)

        for col in ['NAME_INCOME_TYPE', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY']:
            le = encoders[col]
            try:
                 df_input[col] = le.transform(df_input[col])
            except ValueError:
                return jsonify({'error': f'Invalid value for {col}'}), 400

        probs = model.predict_proba(df_input)[0]
        prob_default = probs[1]
        
        credit_score = int(probs[0] * 100)
        
        risk_level = ""
        decision = ""
        explanation = ""
        
        if prob_default < 0.15:
            risk_level = "Low"
            decision = "APPROVE"
            explanation = "Strong financial profile with low default probability."
        elif prob_default <= 0.35:
            risk_level = "Medium"
            decision = "APPROVE (Conditional)"
            explanation = "Moderate risk detected. Approval subject to interest rate adjustment."
        else:
            risk_level = "High"
            decision = "REJECT"
            explanation = "High default risk based on income or employment factors."

        reasons = []
        if income > 250000:
            reasons.append("High Income Stability (+)")
        
        if years_employed > 5:
             reasons.append("Stable Employment Duration (+)")
        elif years_employed < 1:
             reasons.append("Short Employment History (-)")
             
        if own_car == 'Y' or own_realty == 'Y':
            reasons.append("Asset Ownership (+)")

        if reasons:
            explanation += " Key factors: " + "; ".join(reasons)

        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('''
                INSERT INTO credit_applications 
                (amt_income_total, days_employed, name_income_type, cnt_children, 
                flag_own_car, flag_own_realty, predicted_default_probability, 
                credit_score, risk_level, decision)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                income, days_employed, income_type, children, 
                own_car, own_realty, prob_default, 
                credit_score, risk_level, decision
            ))
            conn.commit()
            conn.close()
        except Exception as db_e:
            print("Database Error:", db_e)

        response = {
            'credit_score': credit_score,
            'risk_level': risk_level,
            'decision': decision,
            'explanation': explanation,
            'prob_default_percent': round(prob_default * 100, 1)
        }
        
        return jsonify(response)

    except Exception as e:
        print("Prediction Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
