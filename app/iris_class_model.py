from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import pickle
import numpy as np

iris = load_iris()
X, y = iris.data, iris.target

model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X, y)

test_array = np.array([[7.1, 5.0, 1.0, 0.4]])
prediction = model.predict(test_array)
print(prediction)

with open('iris_model.pkl', 'wb') as file:
    pickle.dump(model, file)

model = pickle.load(open('iris_model.pkl', 'rb'))
