# Copyright(c) Microsoft Corporation.
# Licensed under the MIT license.

library(azuremlsdk)
library(jsonlite)
library(data.table)

ws <- load_workspace_from_config()

# Register the model
model <- register_model(ws, model_path = "outputs", model_name = "attrition-r")

# Reuse the same environment used for training for inference
env <- get_environment(ws, name = 'attrition-env')

# Create inference config
inference_config <- inference_config(
  entry_script = "score.R",
  source_directory = ".",
  environment = env)

# Create ACI deployment config
deployment_config <- aci_webservice_deployment_config(cpu_cores = 1,
                                                      memory_gb = 1)

# Deploy the web service
service <- deploy_model(ws, 
                        'attritionr', 
                        list(model), 
                        inference_config, 
                        deployment_config)
wait_for_deployment(service, show_output = TRUE)
cat(get_webservice_logs(service))

# If you encounter any issue in deploying the webservice, please visit
# https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-troubleshoot-deployment

all_data <- fread('../data/IBM-Employee-Attrition.csv',stringsAsFactors = TRUE)
# remove useless fields 
all_data <- within(all_data, rm(EmployeeCount, Over18, StandardHours, EmployeeNumber))
# make sure attrition is a factor
for (col in c('Attrition')) 
  set(all_data, j=col, value=as.factor(all_data[[col]]))

# sample 10 records
sample <- all_data[sample(.N, 10)]

sample_y <- sample$Attrition
sample[, Attrition := NULL]
sample

# get service from the workspace to refresh the object
service <- get_webservice(ws, name = 'attritionr')

predicted_val <- invoke_webservice(service, toJSON(sample))
predicted_val


