# 🧠 Mental Health Score Prediction from Social Media Usage

Predicting student mental health scores using lifestyle and social media behavior data, built with an end-to-end Scikit-learn + XGBoost pipeline.

## 📌 Overview

This project analyzes how social media usage patterns, study habits, physical activity, and sleep affect the mental health of students. Using a dataset of **5,000 students** across **13 features**, a regression pipeline was built to predict a continuous **Mental Health Score**.

The final model is an **XGBoost Regressor**, tuned for generalization rather than raw training accuracy, achieving strong and *consistent* performance on unseen data.

## 📊 Dataset

| Detail | Value |
|---|---|
| Rows | 5,000 |
| Features | 13 |
| Target | `Mental_Health_Score` (continuous) |

**Feature categories:**
- **Demographics:** Age, Gender, Country, Academic Level
- **Digital behavior:** Most Used Platform, Purpose of Use, Avg. Daily Usage Hours, Daily Unlocks
- **Lifestyle:** Study Hours, Physical Activity Hours, Sleep Hours per Night, Stress Level

## 🔍 Exploratory Data Analysis

- Checked for missing values and duplicate records (duplicates removed)
- Correlation heatmap to identify features most related to `Mental_Health_Score`
- Distribution analysis (histogram + KDE) of the target variable
- Relationship plots between mental health score and key drivers: physical activity, study hours, sleep hours
- Categorical breakdowns: Gender, Country, Purpose of Use, Stress Level

## ⚙️ Preprocessing Pipeline

Built using `ColumnTransformer` for clean, reproducible preprocessing:

| Feature type | Transformation |
|---|---|
| Numerical | `StandardScaler` |
| Categorical | `OneHotEncoder(drop='first', handle_unknown='ignore')` |

## 🤖 Modeling

**Model:** `XGBRegressor` (wrapped in a full `sklearn` Pipeline with preprocessing)

An initial Random Forest baseline showed signs of overfitting (large train/test gap). The model was iterated on — tuning tree depth, learning rate, subsampling, and regularization — to close that gap while preserving predictive performance.

**Final tuned hyperparameters:**
```python
{
    'n_estimators': 500,
    'max_depth': 4,
    'learning_rate': 0.03,
    'subsample': 0.7,
    'colsample_bytree': 0.6,
    'reg_alpha': 3,
    'reg_lambda': 5,
    'min_child_weight': 5
}
```

## 📈 Results

| Metric | Train | Test |
|---|---|---|
| R² Score | 0.87 | **0.86** |
| MSE | — | 0.26 |
| RMSE | — | 0.51 |

The train/test R² gap is just **0.01**, indicating the model generalizes well to unseen data rather than memorizing the training set.

## 🛠️ Tech Stack

- **Python**, **Pandas**, **NumPy**
- **Matplotlib**, **Seaborn** (EDA & visualization)
- **Scikit-learn** (preprocessing, pipeline, train/test split)
- **XGBoost** (final model)

## 🚀 How to Run

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost
jupyter notebook ml.ipynb
```

## 📁 Project Structure

```
├── ml.ipynb                # Full analysis, preprocessing, modeling & evaluation
├── Student Social Media And Mental Health Impact.csv
└── README.md
```

## 🔮 Future Improvements

- Hyperparameter tuning with `RandomizedSearchCV` / `Optuna` for further optimization
- Feature engineering (interaction terms between usage and sleep/study hours)
- Model comparison with LightGBM and CatBoost
- Deployment as a simple web app (Streamlit/Flask) for interactive predictions

---
*This project is for educational and portfolio purposes. The dataset reflects self-reported survey data and should not be used for clinical or diagnostic purposes.*