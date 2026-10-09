import pickle

import numpy as np
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

with open('model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = pd.DataFrame([int_features], columns=['experience', 'test_score', 'interview_score'])
    prediction = model.predict(final_features)
    output = round(float(prediction[0][0]), 2)
    return render_template('index.html', prediction_text=f'Employee salary should be $ {output}')


if __name__ == '__main__':
    app.run(debug=True)
