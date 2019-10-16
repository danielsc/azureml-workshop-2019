# ### Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

import joblib
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn_pandas import DataFrameMapper
import os
import pandas as pd

os.system('pip freeze')

# +
from azureml.core import Run, Workspace, Experiment
# Check core SDK version number
import azureml.core

print("SDK version:", azureml.core.VERSION)
# -

OUTPUT_DIR='./outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# +
print('load dataset')

run = Run.get_context()
if(run.id.startswith("OfflineRun")):
    ws = Workspace.from_config()
    experiment = Experiment(ws, "Train-Explain-Interactive")
    is_remote_run = False
    run = experiment.start_logging(outputs=None, snapshot_directory=".")
    attritionData = ws.datasets['IBM-Employee-Attrition'].to_pandas_dataframe()
else:
    ws = run.experiment.workspace
    attritionData = run.input_datasets['attrition'].to_pandas_dataframe()
    is_remote_run = True

print(attritionData.head())
# -

# Dropping Employee count as all values are 1 and hence attrition is independent of this feature
attritionData = attritionData.drop(['EmployeeCount'], axis=1)
# Dropping Employee Number since it is merely an identifier
attritionData = attritionData.drop(['EmployeeNumber'], axis=1)

attritionData = attritionData.drop(['Over18'], axis=1)

# Since all values are 80
attritionData = attritionData.drop(['StandardHours'], axis=1)
target = attritionData["Attrition"]

attritionXData = attritionData.drop(['Attrition'], axis=1)

# Creating dummy columns for each categorical feature
categorical = []
for col, value in attritionXData.iteritems():
    if value.dtype == 'object':
        categorical.append(col)

# Store the numerical columns in a list numerical
numerical = attritionXData.columns.difference(categorical)

numeric_transformations = [([f], Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])) for f in numerical]

categorical_transformations = [([f], OneHotEncoder(handle_unknown='ignore', sparse=False)) for f in categorical]

transformations = numeric_transformations + categorical_transformations

# Append classifier to preprocessing pipeline.
# Now we have a full prediction pipeline.
clf = Pipeline(steps=[('preprocessor', DataFrameMapper(transformations)),
                      ('classifier', LogisticRegression(solver='lbfgs'))])

# +
from interpret.ext.blackbox import TabularExplainer
from azureml.contrib.interpret.explanation.explanation_client import ExplanationClient
# create an explanation client to store the explanation (contrib API)
client = ExplanationClient.from_run(run)

# Split data into train and test
x_train, x_test, y_train, y_test = train_test_split(attritionXData,
                                                    target,
                                                    test_size=0.2,
                                                    random_state=0,
                                                    stratify=target)


# +
# write x_test out as a pickle file for later visualization
x_test_pkl = 'x_test.pkl'

joblib.dump(value=x_test, filename=os.path.join(OUTPUT_DIR, x_test_pkl))
run.upload_file('x_test_ibm.pkl', os.path.join(OUTPUT_DIR, x_test_pkl))

print('train model')
# preprocess the data and fit the classification model
clf.fit(x_train, y_train)
model = clf.steps[-1][1]



# +
# save model for use outside the script
model_file_name = 'log_reg.pkl'
joblib.dump(value=clf, filename=os.path.join(OUTPUT_DIR, model_file_name))

# register the model with the model management service for later use
run.upload_file('original_model.pkl', os.path.join(OUTPUT_DIR, model_file_name))
original_model = run.register_model(model_name='amlcompute_deploy_model',
                                    model_path='original_model.pkl')



# +
print('create explainer')
# create an explainer to validate or debug the model
tabular_explainer = TabularExplainer(model,
                                     initialization_examples=x_train,
                                     features=attritionXData.columns,
                                     classes=["Not leaving", "leaving"],
                                     transformations=transformations)

# explain overall model predictions (global explanation)
# passing in test dataset for evaluation examples - note it must be a representative sample of the original data
# more data (e.g. x_train) will likely lead to higher accuracy, but at a time cost
global_explanation = tabular_explainer.explain_global(x_test)

print('upload explanation')
# uploading model explanation data for storage or visualization
comment = 'Global explanation on classification model trained on IBM employee attrition dataset'
client.upload_model_explanation(global_explanation, comment=comment)

# -



if not is_remote_run:
    run.complete()

print('completed')

