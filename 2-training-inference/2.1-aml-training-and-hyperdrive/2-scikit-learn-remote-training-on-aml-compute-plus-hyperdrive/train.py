import joblib
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn_pandas import DataFrameMapper
import os
import sklearn_pandas
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import azureml.core

import argparse
from azureml.core import Run, Workspace, Experiment

os.system('pip freeze')

# If you would like to use Azure ML's tracking and metrics capabilities, you will have to add Azure ML code inside your training script:
# In this train.py script we will log some metrics to our Azure ML run. To do so, we will access the Azure ML Run object within the script:
from azureml.core.run import Run
run = Run.get_context()

# Check library versions
print("SDK version:", azureml.core.VERSION)
print('The scikit-learn version is {}.'.format(sklearn.__version__))
print('The joblib version is {}.'.format(joblib.__version__))
print('The pandas version is {}.'.format(pd.__version__))
print('The sklearn_pandas version is {}.'.format(sklearn_pandas.__version__))

# Get Script Arguments for the hyper-parameters
parser = argparse.ArgumentParser(description="Training Script")
parser.add_argument('--solver', type=str, default='lbfgs',
                    help='Algorithm to use for the ML task')
parser.add_argument('--penalty', type=str, default='l2',
                    help='Used to specify the norm used in the penalization')

args, leftovers = parser.parse_known_args()
# args = parser.parse_args()
    
print('The Scikit-Learn algorithm to use is {}.'.format(np.str(args.solver)))
print('The penalty used is {}.'.format(np.str(args.penalty)))
      
print('Loading dataset')
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

# --- Data cleaning -----------------------------------------------

# Dropping Employee count as all values are 1 and hence attrition is independent of this feature
attritionData = attritionData.drop(['EmployeeCount'], axis=1)
# Dropping Employee Number since it is merely an identifier
attritionData = attritionData.drop(['EmployeeNumber'], axis=1)

attritionData = attritionData.drop(['Over18'], axis=1)

# Since all values are 80
attritionData = attritionData.drop(['StandardHours'], axis=1)
target = attritionData["Attrition"]

attritionXData = attritionData.drop(['Attrition'], axis=1)
# -----------------------------------------------------------------

# --- Data Transformations -----------------------------------------------

# Collect the categorical column names in separate list
categorical = []
for col, value in attritionXData.iteritems():
    if value.dtype == 'object':
        categorical.append(col)
        
# Collect the numerical column names in separate list
numerical = attritionXData.columns.difference(categorical)

# Create data processing pipelines
numeric_transformations = [([f], Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])) for f in numerical]

categorical_transformations = [([f], OneHotEncoder(handle_unknown='ignore', sparse=False)) for f in categorical]

transformations_pipeline = numeric_transformations + categorical_transformations

# Append classifier algorithm to preprocessing pipeline.
# Now we have a full prediction pipeline.
model_pipeline = Pipeline(steps=[('preprocessor', DataFrameMapper(transformations_pipeline)),
                                 ('classifier', LogisticRegression(solver=args.solver, penalty=args.penalty))])

# Check Scikit-Learn docs to see the hyper-parameters available for the LogisticRegression:
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html


# +

# Split data into train and test
x_train, x_test, y_train, y_test = train_test_split(attritionXData,
                                                    target,
                                                    test_size=0.2,
                                                    random_state=0,
                                                    stratify=target)


# +

OUTPUT_DIR='./outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# write y_test out (placed into /outputs) as a pickle file for later external usage
y_test_pkl = 'y_test.pkl'
joblib.dump(value=y_test, filename=os.path.join(OUTPUT_DIR, y_test_pkl))

# write x_test out (placed into /outputs) as a pickle file for later external usage
x_test_pkl = 'x_test.pkl'
joblib.dump(value=x_test, filename=os.path.join(OUTPUT_DIR, x_test_pkl))
# (CDLTLL No needed) run.upload_file('x_test_ibm.pkl', os.path.join(OUTPUT_DIR, x_test_pkl))

print('Training the model')
# preprocess the data and train the classification model
trained_model = model_pipeline.fit(x_train, y_train)

# (CDLTLL - Not used)
# model = model_pipeline.steps[-1][1]

# +
# Calculate Accuracy for x_test

# Make Multiple Predictions
y_predictions = trained_model.predict(x_test)

accuracy = accuracy_score(y_test, y_predictions)
# (Method 2 with svm model) accuracy = svm_model_linear.score(x_test, y_test)

print('Accuracy of LogisticRegression classifier on test set: {:.2f}'.format(accuracy))

# Set Accuracy metric to the run.log to be used later by Azure ML's tracking and metrics capabilities
run.log("Accuracy", float(accuracy))

# creating a confusion matrix
cm = confusion_matrix(y_test, y_predictions)
print(cm)

# Save the model as .pkl file

# +
# save model file to the outputs/ folder to use outside the script
model_file_name = 'classif-empl-attrition.pkl'
joblib.dump(value=trained_model, filename=os.path.join(OUTPUT_DIR, model_file_name))

# Upload model .pkl file to the ROOT folder
# run.upload_file('model_copy.pkl', os.path.join(OUTPUT_DIR, model_file_name))

# register the model with the model management service for later use
# (CDLTLL) Not needed here. I can register the model after the remote run, from the outside, depending on the results 
#
# original_model = run.register_model(model_name='classif-empl-attrition-aml-comp',
#                                     model_path=os.path.join(OUTPUT_DIR, model_file_name))

# -

if not is_remote_run:
    run.complete()

print('completed')

