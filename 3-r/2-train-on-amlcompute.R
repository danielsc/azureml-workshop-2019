# run setup.R to setup workspace for the first time
# set working directory to current file location prior to running this script
library("azuremlsdk")

ws <- load_workspace_from_config()

ds <- get_default_datastore(ws)

# upload attrition data set to the datastore
upload_files_to_datastore(ds,
                          list("../data/IBM-Employee-Attrition.csv"),
                          target_path = 'attriton',
                          overwrite = TRUE)

# create aml compute
cluster_name <- "cpu"
compute_target <- get_compute(ws, cluster_name = cluster_name)
if (is.null(compute_target)) {
  vm_size <- "STANDARD_D2_V2"
  compute_target <- create_aml_compute(workspace = ws,
                                       cluster_name = cluster_name,
                                       vm_size = vm_size,
                                       max_nodes = 1)
}

# define estimator
est <- estimator(source_directory = ".",
                 entry_script = "train.R",
                 script_params = list("--data" = ds$path('attrition/IBM-Employee-Attrition.csv')),
                 compute_target = compute_target,
                 cran_packages = c("caret", "optparse", "e1071", "kernlab"))

experiment_name <- "train-r-script-on-amlcompute"
exp <- experiment(ws, experiment_name)

run <- submit_experiment(exp, est)
view_run_details(run)
wait_for_run_completion(run, show_output = TRUE)

metrics <- get_run_metrics(run)
metrics

# delete cluster
delete_compute(compute_target)
