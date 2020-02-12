<!-- #region -->
## AzureML and R

This module will show how to use Azure ML with R. The Azure ML SDK for R is available today in public preview. The SDK is open-sourced and developed on [GitHub](https://github.com/Azure/azureml-sdk-for-r) and also available on [CRAN](https://cran.r-project.org/web/packages/azuremlsdk/index.html).

In this module we will be using both the Jupyter and the RStudio instances that are installed on the [Compute instance](https://docs.microsoft.com/en-us/azure/machine-learning/concept-compute-instance) you set up in the [first module](https://github.com/danielsc/azureml-workshop-2019/blob/master/1-workspace-concepts/1-setup-compute.md) of the workshop.

Before running through this module, please execute the setup script to make sure all required components are installed by opening a Jupyter terminal window and running the following command in the subdirectory `5-r` of this repository:

```
sudo Rscript 0-setup.R
```

If you get a `"Would you like to install Miniconda? [Y/n]"` prompt please enter `"n"`.

<!-- #endregion -->


