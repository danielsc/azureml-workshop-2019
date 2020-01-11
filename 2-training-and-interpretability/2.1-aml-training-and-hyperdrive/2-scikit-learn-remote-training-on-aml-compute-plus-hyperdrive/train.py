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
                                 ('classifier', LogisticRegression(solver='lbfgs'))])

# (CDLTLL) Why are we using a LogisticRegression here instead of SVC?


# +

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
# preprocess the data and train the classification model
model_pipeline.fit(x_train, y_train)
model = model_pipeline.steps[-1][1]



# +
# save model for use outside the script
model_file_name = 'log_reg.pkl'
joblib.dump(value=model_pipeline, filename=os.path.join(OUTPUT_DIR, model_file_name))

# register the model with the model management service for later use
run.upload_file('original_model.pkl', os.path.join(OUTPUT_DIR, model_file_name))
original_model = run.register_model(model_name='amlcompute_deploy_model',
                                    model_path='original_model.pkl')


# -

if not is_remote_run:
    run.complete()

print('completed')

