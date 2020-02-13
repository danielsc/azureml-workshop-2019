# +
## Installing prerequisites for the R part of the workshop
# Please run this script with:
#
#     sudo Rscript 0-setup.R
# -

# Install the azuremlsdk package
install.packages('remotes')

remotes::install_cran('azuremlsdk', repos = 'https://cloud.r-project.org/')

# Install additional packages that will be used in this module
install.packages(c('data.table'))

# Only install the following packages if you want to run the training script train.R locally
# You will not need these packages if you run train.R on your remote AmlCompute cluster
# install.packages(c('caret','kernlab','e1071'))

# Use the azuremlsdk library to install the Python SDK
azuremlsdk::install_azureml(envname = 'r-reticulate')




