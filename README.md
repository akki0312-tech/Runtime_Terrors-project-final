# Credit Scoring System for Financial Inclusion

A hackathon project that uses machine learning to help people without traditional credit history get access to loans.

## The Problem

Lots of people in India (and around the world) don't have credit cards or bank loans, so they don't have a "credit score". This makes it really hard for them to get loans, even if they're actually reliable borrowers. They end up going to informal lenders who charge crazy high interest rates.

## Our Solution

We built an AI system that looks at different kinds of data to predict if someone is likely to repay a loan:
- Income and employment history
- Whether they own assets (car, house)
- Family size
- Type of employment

The model gives them a credit score (0-100) and decides whether to approve, conditionally approve, or reject their loan application.

## Tech Stack

- **Backend**: Python Flask
- **ML Model**: Random Forest Classifier (scikit-learn)
- **Database**: SQLite
- **Frontend**: HTML/CSS/JavaScript
- **Dataset**: Home Credit Default Risk dataset

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Train the model (already done, but if you want to retrain):
```bash
python train_model.py
```

3. Run the app:
```bash
python app.py
```

4. Open your browser and go to: `http://127.0.0.1:5000`

## Features

- **Home Page**: Explains the problem and solution
- **Assessment Page**: Enter applicant details and get instant credit score
- **History Page**: See all past assessments (loaded from the dataset)
- **Fairness Page**: Explains what data we use and don't use

## Model Performance

- Accuracy: 84.4%
- Dataset: 5000 samples from Home Credit Default Risk
- Features: 6 (income, employment, assets, children, etc.)

## Demo

Use the demo buttons on the assessment page to try:
1. **Good Credit Example**: State servant with stable income and assets → Low Risk
2. **Poor Credit Example**: Student with low income and no assets → High Risk

## Important Notes

- This is a **demonstration project** for educational purposes
- We don't use discriminatory features (gender, religion, caste, etc.)
- Real deployment would need proper security, compliance, and human oversight

## Impact

If this were deployed at scale, it could help millions of unbanked people access credit based on their actual reliability, not just their formal banking history. This is especially important for small business owners, daily wage workers, and others in the informal economy.

---
The project is live on - https://runtime-terrors-project-final.onrender.com/
Built for Netweb AI for Public Good Hackathon - Team Runtime Terrors
