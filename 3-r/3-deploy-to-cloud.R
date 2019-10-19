# Copyright(c) Microsoft Corporation.
# Licensed under the MIT license.

library("azuremlsdk")
library("jsonlite")

ws <- load_workspace_from_config()

# register the model
model <- register_model(ws, model_path = "outputs/model.rds", model_name = "attrition-r")
r_env <- r_environment(name = "r_env", cran_packages = c("caret", "optparse", "e1071", "kernlab"))

# create inference config
inference_config <- inference_config(
  entry_script = "score.R",
  source_directory = ".",
  environment = r_env)

# create ACI deployment config
deployment_config <- aci_webservice_deployment_config(cpu_cores = 1,
                                                      memory_gb = 1)

# deploy the webservice
service <- deploy_model(ws, 
                        'attritionr', 
                        list(model), 
                        inference_config, 
                        deployment_config)
wait_for_deployment(service, show_output = TRUE)

# If you encounter any issue in deploying the webservice, please visit
# https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-troubleshoot-deployment

all_data <- fread('../data/IBM-Employee-Attrition.csv',stringsAsFactors = TRUE)
# remove useless fields 
all_data = within(all_data, rm(EmployeeCount, Over18, StandardHours, EmployeeNumber))
# make sure attrition is a factor
for (col in c('Attrition')) 
  set(all_data, j=col, value=as.factor(all_data[[col]]))

# sample 10 records
sample = all_data[sample(.N, 10)]

sample_y = sample$Attrition
sample[, Attrition := NULL]
sample

predicted_val <- invoke_webservice(service, toJSON(sample))
predicted_val

cat(service$get_logs())
