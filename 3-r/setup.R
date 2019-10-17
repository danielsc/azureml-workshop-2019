# install jupyter kernel for R
install.packages(c('repr', 'IRdisplay', 'IRkernel'), type='source', lib='/usr/local/lib/R/site-library', repos='http://cran.us.r-project.org')
IRkernel::installspec()

# install azureml sdk for R
install.packages("remotes", repos = "http://cran.rstudio.com")
remotes::install_github('https://github.com/Azure/azureml-sdk-for-r')
library(azuremlsdk)
install_azureml()

# other stuff used
install.packages('data.table')

# fix mounting issue for datasets
system('/anaconda/envs/r-azureml/bin/pip install azureml-dataprep[pandas]')

