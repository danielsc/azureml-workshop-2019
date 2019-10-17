
import pandas as pd
from sklearn.externals import joblib
from azureml.core.model import Model

import json
import pickle
import numpy as np

from inference_schema.schema_decorators import input_schema, output_schema
from inference_schema.parameter_types.numpy_parameter_type import NumpyParameterType
from inference_schema.parameter_types.pandas_parameter_type import PandasParameterType


input_sample = pd.DataFrame(data=[{'Age': 41, 'BusinessTravel': 'Travel_Rarely', 'DailyRate': 1102, 'Department': 'Sales', 'DistanceFromHome': 1, 'Education': 2, 'EducationField': 'Life Sciences', 'EnvironmentSatisfaction': 2, 'Gender': 'Female', 'HourlyRate': 94, 'JobInvolvement': 3, 'JobLevel': 2, 'JobRole': 'Sales Executive', 'JobSatisfaction': 4, 'MaritalStatus': 'Single', 'MonthlyIncome': 5993, 'MonthlyRate': 19479, 'NumCompaniesWorked': 8, 'OverTime': 'No', 'PercentSalaryHike': 11, 'PerformanceRating': 3, 'RelationshipSatisfaction': 1, 'StockOptionLevel': 0, 'TotalWorkingYears': 8, 'TrainingTimesLastYear': 0, 'WorkLifeBalance': 1, 'YearsAtCompany': 6, 'YearsInCurrentRole': 4, 'YearsSinceLastPromotion': 0, 'YearsWithCurrManager': 5}])
output_sample = np.array([0])


def init():
    global model
    # This name is model.id of model that we want to deploy deserialize the model file back
    # into a sklearn model
    model_path = Model.get_model_path('IBM_attrition_model')
    model = joblib.load(model_path)


@input_schema('data', PandasParameterType(input_sample))
@output_schema(NumpyParameterType(output_sample))
def run(data):
    try:
        result = model.predict(data)
        return json.dumps({"result": result.tolist()})
    except Exception as e:
        result = str(e)
        return json.dumps({"error": result})
