import joblib
from fastapi import FastAPI 
from pydantic import BaseModel,Field
model=joblib.load('mental_health_model.pkl')
class data(BaseModel):
    Age: int=Field(..., gt=0, description="Age must be a positive integer",examples=[25])
    Gender: str=Field(..., description="Gender must be a string",examples=["Male"])
    Country: str=Field(..., description="Country must be a string",examples=["USA"])
    Academic_Level: str=Field(..., description="Academic level must be a string",examples=["Bachelor's"])
    Most_Used_Platform: str=Field(..., description="Most used platform must be a string",examples=["Instagram"])
    Purpose_Of_Use: str=Field(..., description="Purpose of use must be a string",examples=["Social Media"])
    Avg_Daily_Usage_Hours: float=Field(..., description="Average daily usage hours must be a float",examples=[3.5])
    Daily_Unlocks: int=Field(..., description="Daily unlocks must be an integer",examples=[10])
    Study_Hours: float=Field(..., description="Study hours must be a float",examples=[2.0])
    Physical_Activity_Hours: float=Field(..., description="Physical activity hours must be a float",examples=[1.5])
    Sleep_Hours_Per_Night: float=Field(..., description="Sleep hours per night must be a float",examples=[7.0])
    Stress_Level: str=Field(..., description="Stress level must be a string",examples=["Low"])
app=FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome to the Mental Health Score Prediction API"}
@app.post("/predict")
def predict(data: data):

    input_data = [[
        data.Age,
        data.Gender,
        data.Country,
        data.Academic_Level,
        data.Most_Used_Platform,
        data.Purpose_Of_Use,
        data.Avg_Daily_Usage_Hours,
        data.Daily_Unlocks,
        data.Study_Hours,
        data.Physical_Activity_Hours,
        data.Sleep_Hours_Per_Night,
        data.Stress_Level
    ]]

    prediction = model.predict(input_data)

    return {
        "Mental_Health_Score": prediction[0]
    }
