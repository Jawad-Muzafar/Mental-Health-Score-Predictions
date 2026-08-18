import logging
import os
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "mental_health_model.pkl")

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("mental_health_api")

# ---------------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------------
try:
    model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise RuntimeError(f"Failed to load model: {e}")


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class PredictionInput(BaseModel):
    Age: int = Field(..., gt=0, description="Age must be a positive integer", examples=[25])
    Gender: Literal["Male", "Female", "Other"] = Field(..., examples=["Male"])
    Country: str = Field(..., description="Country must be a string", examples=["USA"])
    Academic_Level: Literal["High School", "Bachelor's", "Master's", "PhD"] = Field(
        ..., examples=["Bachelor's"]
    )
    Most_Used_Platform: str = Field(..., description="Most used platform", examples=["Instagram"])
    Purpose_Of_Use: str = Field(..., description="Purpose of use", examples=["Social Media"])
    Avg_Daily_Usage_Hours: float = Field(..., ge=0, le=24, examples=[3.5])
    Daily_Unlocks: int = Field(..., ge=0, examples=[10])
    Study_Hours: float = Field(..., ge=0, le=24, examples=[2.0])
    Physical_Activity_Hours: float = Field(..., ge=0, le=24, examples=[1.5])
    Sleep_Hours_Per_Night: float = Field(..., ge=0, le=24, examples=[7.0])
    Stress_Level: Literal["Low", "Medium", "High"] = Field(..., examples=["Low"])


class PredictionOutput(BaseModel):
    Mental_Health_Score: float


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(title="Mental Health Score Prediction API")

# CORS - allows your HTML/JS frontend (even if opened from a different
# origin/port) to call this API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # In production, replace "*" with your real frontend domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/api")
def read_root():
    return {"message": "Welcome to the Mental Health Score Prediction API"}


@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    logger.info(f"Received prediction request: {data.model_dump()}")

    input_df = pd.DataFrame([{
        "Age": data.Age,
        "Gender": data.Gender,
        "Country": data.Country,
        "Academic_Level": data.Academic_Level,
        "Most_Used_Platform": data.Most_Used_Platform,
        "Purpose_Of_Use": data.Purpose_Of_Use,
        "Avg_Daily_Usage_Hours": data.Avg_Daily_Usage_Hours,
        "Daily_Unlocks": data.Daily_Unlocks,
        "Study_Hours": data.Study_Hours,
        "Physical_Activity_Hours": data.Physical_Activity_Hours,
        "Sleep_Hours_Per_Night": data.Sleep_Hours_Per_Night,
        "Stress_Level": data.Stress_Level,
    }])

    try:
        prediction = model.predict(input_df)
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    score = round(float(prediction[0]), 2)
    logger.info(f"Prediction result: {score}")

    return PredictionOutput(Mental_Health_Score=score)


# ---------------------------------------------------------------------------
# Serve the frontend (HTML/CSS/JS) at "/"
# The actual frontend files live in the project root, not inside a static folder.
# ---------------------------------------------------------------------------
app.mount("/", StaticFiles(directory=BASE_DIR, html=True), name="static")