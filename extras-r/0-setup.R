# +
## Installing prerequisites for the R part of the workshop
# please run this script with
#
#     sudo Rscript 0-setup.R
# -

# install azureml sdk for R
install.packages("remotes", repos = "http://cran.rstudio.com")

remotes::install_github('https://github.com/Azure/azureml-sdk-for-r')

# other stuff used
install.packages(c('data.table', 'caret','kernlab','e1071'))




