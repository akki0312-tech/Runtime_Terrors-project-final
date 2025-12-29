import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

def train_model():
    print("Loading data...")
    df = pd.read_csv('credit_data.csv')

    le_dict = {}
    categorical_cols = ['NAME_INCOME_TYPE', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY']

    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        le_dict[col] = le
    
    feature_cols = ['AMT_INCOME_TOTAL', 'DAYS_EMPLOYED', 'NAME_INCOME_TYPE', 
                    'CNT_CHILDREN', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY']
    
    missing_cols = [c for c in feature_cols + ['TARGET'] if c not in df.columns]
    if missing_cols:
        print(f"Error: Missing columns in CSV: {missing_cols}")
        return

    X = df[feature_cols]
    y = df['TARGET']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training Random Forest Classifier...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    joblib.dump(rf, 'model.pkl')
    joblib.dump(le_dict, 'encoders.pkl')
    print("Model and encoders saved to disk.")

if __name__ == "__main__":
    train_model()
