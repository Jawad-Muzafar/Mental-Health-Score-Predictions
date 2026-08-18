# 🧠 Mental Health Score Prediction

A machine learning project that predicts a student's mental health score based on digital habits, lifestyle factors, and academic behavior. The project includes a trained model, a FastAPI backend, and a modern frontend dashboard for live predictions.

## 📌 Overview

This project analyzes how social media usage, study hours, sleep, stress, and physical activity influence mental wellbeing. The model is trained on student survey data and predicts a continuous mental health score from 0 to 10.

The repository now includes:
- a full ML notebook for training and evaluation
- a saved model file for inference
- a FastAPI API for prediction requests
- a polished frontend interface served directly from the project root

## 🧪 Dataset

The project uses a dataset named:
- `Student Social Media And Mental Health Impact.csv`

It contains student-level data across demographic, digital behavior, and lifestyle features.

Key feature groups:
- Demographics: Age, Gender, Country, Academic Level
- Digital usage: Most Used Platform, Purpose of Use, Avg Daily Usage Hours, Daily Unlocks
- Lifestyle: Study Hours, Physical Activity Hours, Sleep Hours, Stress Level
- Target: `Mental_Health_Score`

## 🤖 Machine Learning Pipeline

The model was built with:
- preprocessing via `ColumnTransformer`
- numerical scaling with `StandardScaler`
- categorical encoding with `OneHotEncoder`
- final regressor using `XGBoost`

This setup allows the app to accept user input in a structured form and return a predicted mental health score.

## 🌐 Web App

The project now includes a FastAPI app and browser UI.

### API endpoints
- `GET /api` → API welcome message
- `POST /predict` → submit form data and receive a score
- root route `/` serves the frontend HTML page

### Frontend
The app serves the static files from the project root, so the following files are used by the browser:
- `index.html`
- `style.css`
- `script.js`

## 🚀 Run the App

From the project root:

```bash
pip install fastapi uvicorn pandas joblib xgboost scikit-learn
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

## 🔍 Local Validation

The app was verified to serve successfully:
- `/` → 200 OK
- `/style.css` → 200 OK
- `/script.js` → 200 OK
- `/api` → 200 OK

## 📁 Project Structure

```text
Mental-Health-Score-Predictions/
├── main.py                     # FastAPI app and model loading
├── index.html                  # Frontend page
├── style.css                   # UI styling and animations
├── script.js                   # Frontend form logic and prediction request
├── mental_health_model.pkl     # Trained model
├── ml.ipynb                    # Training and evaluation notebook
├── Student Social Media And Mental Health Impact.csv
├── README.md
└── __pycache__/
```

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- XGBoost
- FastAPI
- JavaScript
- HTML/CSS

## ⚠️ Notes

This project is intended for educational and portfolio use. It should not be used as a clinical diagnostic tool.

---
*Built for student wellbeing prediction and demo deployment.*