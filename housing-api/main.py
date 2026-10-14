import pickle
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Housing Prediction API")

model_path = Path(__file__).parent / "model.pkl"

with open(model_path, "rb") as file:
    model = pickle.load(file)


class HousingInput(BaseModel):
    med_inc: float
    house_age: float
    ave_rooms: float
    ave_bedrms: float


@app.post("/predict")
def predict(data: HousingInput):
    # We Keep this order aligned with train.py: med_inc, house_age, ave_rooms, ave_bedrms.
    features = [[
        data.med_inc,
        data.house_age,
        data.ave_rooms,
        data.ave_bedrms,
    ]]
    prediction = model.predict(features)[0]
    return {"prediction": float(prediction)}
