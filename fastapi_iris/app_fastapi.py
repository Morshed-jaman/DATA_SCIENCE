#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
import contextlib

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


# In[2]:


ml_model = None


# In[3]:


class IrisFeatures(BaseModel):
    s_length: float
    s_width: float
    p_length: float
    p_width: float


# In[4]:


@contextlib.asynccontextmanager
async def lifespan(app:FastAPI):

    global ml_model
    try:
        with open('iris_model.pkl', 'rb') as file:
            ml_model = pickle.load(file)

    except Exception as e:
        print('Model file is not available')

    yield


# In[5]:


app = FastAPI(
    title = 'Iris Classification',
    description = 'Iris API for classification',
    version = '1.0.0',
    lifespan = lifespan    
)


# In[6]:


@app.post('/predict', response_model = List[int])
def predict(features: IrisFeatures):
    if ml_model is None:
        return {'error': 'Model not found'}

    data = [[
        features.s_length,
        features.s_width,
        features.p_length,
        features.p_width
    ]]

    prediction = ml_model.predict(data).tolist()

    return prediction

