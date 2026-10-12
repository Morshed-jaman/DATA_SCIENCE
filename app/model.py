#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from word2number import w2n
import pickle
from sklearn.linear_model import LinearRegression


dataset = pd.read_csv('hiring.csv')
print(dataset)

dataset['experience'] = dataset['experience'].fillna('zero')
print(dataset)

dataset['experience'] = dataset['experience'].apply(w2n.word_to_num)
print(dataset)

dataset['test_score'] = dataset['test_score'].fillna(dataset['test_score'].mean())
print(dataset)

X = dataset.iloc[:, :3]
print(X)

y = dataset.iloc[:, 3:4]
print(y)

regressor = LinearRegression()
regressor.fit(X, y)

test_df = pd.DataFrame([[2, 9, 7], [5, 8, 6]], columns=['experience', 'test_score', 'interview_score'])
print(regressor.predict(test_df))

pickle.dump(regressor, open('model.pkl', 'wb'))

model = pickle.load(open('model.pkl', 'rb'))
print(model.predict(test_df))
