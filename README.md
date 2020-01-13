# Azure ML E2E Workshop

## Target Audience
Anyone who wants a comprehensive E2E understanding of Azure ML.

## Key Goals
1.	Understand the product E2E
2.	Ensure that the work we are doing in Mn will address key gaps in usability / E2E user experience
3.	Open bugs, fix docs & ensure commitments from product area leads on whether / how those bugs will be fixed

## Agenda (day 1)
- **8-9am: Coffee / breakfast / arrive**

### 9-9:30 || Intro (run through Azure ML quick pitch / value prop)** 
- https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-azure-machine-learning-architecture

### 9:30-1030 || Module 1, infra setup, ARM, workspace setup, computes, datastores, setup**
- https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-manage-workspace
- https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-configure-environment
- https://docs.microsoft.com/en-us/azure/machine-learning/service/tutorial-1st-experiment-sdk-setup

### 10:30-12:30 || Module 2, Datasets, Model Training (AML, HyperDrive and AutoML), Model Interpretability**

##### Notebooks to run and research:

AML training, HyperDrive and Interpretability:
- [Notebook for plain vanilla Scikit-Learn model training in AML local compute (AML VM)](https://github.com/danielsc/azureml-workshop-2019/blob/master/2-training-and-interpretability/2.1-aml-training-and-hyperdrive/1-scikit-learn-local-training-on-notebook-plus-aml-ds-and-log/binayclassification-employee-attrition-notebook.ipynb) 
- [Notebook for Scikit-Learn model training in AML remote compute and HyperDrive](https://github.com/danielsc/azureml-workshop-2019/blob/master/2-training-and-interpretability/2.1-aml-training-and-hyperdrive/2-scikit-learn-remote-training-on-aml-compute-plus-hyperdrive/binayclassification-employee-attrition-aml-compute-notebook.ipynb) 
- [Notebook for Model Interpretability in AML](https://github.com/danielsc/azureml-workshop-2019/blob/master/2-training-and-interpretability/2.2-aml-interpretability/1-simple-feature-transformations-explain-local.ipynb)

Automated ML:
- [Notebook for AutoML local compute](https://github.com/danielsc/azureml-workshop-2019/blob/master/2-training-and-interpretability/2.1-aml-training-and-hyperdrive/2-scikit-learn-remote-training-on-aml-compute-plus-hyperdrive/binayclassification-employee-attrition-aml-compute-notebook.ipynb)
- [Notebook for AutoML remote compute](https://github.com/danielsc/azureml-workshop-2019/blob/master/2-training-and-interpretability/2.1-aml-training-and-hyperdrive/2-scikit-learn-remote-training-on-aml-compute-plus-hyperdrive/binayclassification-employee-attrition-aml-compute-notebook.ipynb)

Complementary tutorials and HowTo:

https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-version-track-datasets
https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-train-with-datasets


#### **Tutorials for Module 2**
- https://docs.microsoft.com/en-us/azure/machine-learning/service/tutorial-train-models-with-aml
- https://github.com/danielsc/azureml-workshop-2019/blob/master/1-new-workspace/3-automl.md
- https://github.com/danielsc/azureml-workshop-2019/blob/master/2-interpretability/2-explain-model-on-amlcompute.ipynb

#### Stretch Goal for Module 2: Get interpretability working on the scikit-learn training job.**

### **1-4 || Module 3, MLOps (model management, deployment, inference, automation)**
- https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-model-management-and-deployment
- https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-deploy-and-where
- EventGrid https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-event-grid-integration

#### **Tutorials for MLOps**
- https://docs.microsoft.com/en-us/azure/machine-learning/service/tutorial-pipeline-batch-scoring-classification
- https://docs.microsoft.com/en-us/azure/machine-learning/service/tutorial-deploy-models-with-aml
- https://docs.microsoft.com/en-us/azure/machine-learning/service/tutorial-train-deploy-model-cli
- https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-use-event-grid

#### Stretch Goal for Module 3 - Set up automated training and deployment on a schedule.**

### **4-5 || Module 4, Enterprise Readiness**
- Azure Monitor https://docs.microsoft.com/en-us/azure/machine-learning/service/monitor-azure-machine-learning
- RBAC https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-enterprise-security
- https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-assign-roles
- Limits service https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-manage-quotas
- VNET https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-enable-virtual-network

