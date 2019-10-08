import pandas as pd
from sklearn.externals import joblib
from azureml.core.model import Model

def init():

    global original_model
    
    # Retrieve the path to the model file using the model name
    original_model_path = Model.get_model_path('IBM-attrition-model')
    
    original_model = joblib.load(original_model_path)
    
def run(raw_data):
    # Get predictions and explanations for each data point
    data = pd.read_json(raw_data)
    # Make prediction
    predictions = original_model.predict(data)
    return {'predictions': predictions.tolist()}