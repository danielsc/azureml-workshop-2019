# Azure ML E2E Workshop

## Target Audience
Anyone who wants a comprehensive E2E understanding of Azure ML.

## Key Goals
1.	Understand the product E2E
2.	Ensure that the work we are doing in Mn will address key gaps in usability / E2E user experience
3.	Open bugs, fix docs & ensure commitments from product area leads on whether / how those bugs will be fixed

## Agenda

### Workspace Concepts: infra setup, ARM, workspace setup, computes, datastores, setup**
1. [Set up your workspace and compute](./1-workspace-concepts/1-setup-compute.md)
1. [Register a dataset](./1-workspace-concepts/2-dataset.md)
1. [Run AutoML from the UI](./1-workspace-concepts/3-automl.md)
1. [Compute Instance - Clone Git Repo](./1-workspace-concepts/5-clone-git-repo.md)


### Datasets, Model Training (AML, HyperDrive and AutoML), Model Inference**

#### Notebooks to run and research:

AML training, HyperDrive and Interpretability:
- [Notebook for plain vanilla Scikit-Learn model training in AML local compute (AML VM)](./2-training-inference/2.1-aml-training-and-hyperdrive/1-scikit-learn-local-training-on-notebook-plus-aml-ds-and-log/binayclassification-employee-attrition-notebook.ipynb)
- [Notebook for Scikit-Learn model training in AML remote compute and HyperDrive](./2-training-inference/2.1-aml-training-and-hyperdrive/2-scikit-learn-remote-training-on-aml-compute-plus-hyperdrive/binayclassification-employee-attrition-aml-compute-notebook.ipynb) 
- [Notebook for Model Interpretability in AML](./2-training-inference/2.2-aml-interpretability/1-simple-feature-transformations-explain-local.ipynb)

Automated ML:
- [Notebook for AutoML local compute](./2-training-inference/2.1-aml-training-and-hyperdrive/2-scikit-learn-remote-training-on-aml-compute-plus-hyperdrive/binayclassification-employee-attrition-aml-compute-notebook.ipynb)
- [Notebook for AutoML remote compute](./2-training-inference/2.1-aml-training-and-hyperdrive/2-scikit-learn-remote-training-on-aml-compute-plus-hyperdrive/binayclassification-employee-attrition-aml-compute-notebook.ipynb)

Pipelines & Batch Inference
- [Use a model for batch inference](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/machine-learning-pipelines/parallel-run/tabular-dataset-inference-iris.ipynb)


### MLOps (model management, deployment, inference, automation)

#### **Tutorials for MLOps**
- [Deploy a model](./3-mlops/deploy-attrition-model.ipynb)
- [Automate training & deployment](./3-mlops/mlopsworkshop.md)
- [Create automation workflow with EventGrid](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-use-event-grid#sample-scenarios)

### Enterprise Readiness
- Azure Monitor https://docs.microsoft.com/en-us/azure/machine-learning/service/monitor-azure-machine-learning
- RBAC https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-enterprise-security
- https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-assign-roles
- Limits service https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-manage-quotas
- VNET https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-enable-virtual-network

