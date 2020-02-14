# set working directory to current file location prior to running this script
library(azuremlsdk)

ws <- load_workspace_from_config()

ds <- get_default_datastore(ws)

# Upload attrition data set to the datastore
upload_files_to_datastore(ds,
                          list("../data/IBM-Employee-Attrition.csv"),
                          target_path = 'attrition',
                          overwrite = TRUE)

# Create an AmlCompute cluster or retrieve an existing one
cluster_name <- 'cpu-cluster'
compute_target <- get_compute(ws, cluster_name = cluster_name)
if (is.null(compute_target)) {
  vm_size <- 'STANDARD_D2_V2'
  compute_target <- create_aml_compute(workspace = ws,
                                       cluster_name = cluster_name,
                                       vm_size = vm_size,
                                       max_nodes = 1)
  
  wait_for_provisioning_completion(compute_target, show_output = TRUE)
}
compute_target

# Define the environment for your training run
env <- r_environment(name = 'attrition-env', cran_packages = c('kernlab'))

# Register the environment to your workspace
register_environment(env, ws)

# Define an estimator to specify your training run configuration
est <- estimator(source_directory = '.',
                 entry_script = 'train.R',
                 script_params = list('--data' = ds$path('attrition/IBM-Employee-Attrition.csv')),
                 compute_target = compute_target,
                 environment = env
                 )

exp <- experiment(ws, name = 'train-r-script-on-amlcompute')

run <- submit_experiment(exp, est)
wait_for_run_completion(run, show_output = TRUE)

metrics <- get_run_metrics(run)
metrics

# Delete the cluster if you no longer need it
# delete_compute(compute_target)
