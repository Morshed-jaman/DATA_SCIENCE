import pickle
from pathlib import Path

from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import GradientBoostingRegressor

# Load the dataset.
data = fetch_california_housing()

# Keep exactly the four features required by the question:
# MedInc, HouseAge, AveRooms, AveBedrms
X = data.data[:, :4]
y = data.target

# Train the model.
model = GradientBoostingRegressor(random_state=42)
model.fit(X, y)

# Save this trained model beside this script.
model_path = Path(__file__).parent / "model.pkl"

with open(model_path, "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully:", model_path)

sample = [[8.52, 41.0, 6.98, 1.02]]
print("Sample prediction:", float(model.predict(sample)[0]))