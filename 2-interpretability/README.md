# Model Interpretability

In this module, you will learn how to explain why your model made the predictions it did with the interpretability package of the Azure Machine Learning Python SDK (Preview).

Using the classes and methods in the SDK, you can get:

- Feature importance values for both raw and engineered features
- Interpretability on real-world datasets at scale, during training and inference.
- Interactive visualizations to aid you in the discovery of patterns in data and explanations at training time

During the training phase of the development cycle, model designers and evaluators can use interpretability output of a model to verify hypotheses and build trust with stakeholders. They also use the insights into the model for debugging, validating model behavior matches their objectives, and to check for bias.

In machine learning, features are the data fields used to predict a target data point. For example, to predict credit risk, data fields for age, account size, and account age might be used. In this case, age, account size, and account age are features. Feature importance tells you how each data field affected the model's predictions. For example, age may be heavily used in the prediction while account size and age don't affect the prediction accuracy significantly. This process allows data scientists to explain resulting predictions, so that stakeholders have visibility into what data points are most important in the model.

Using these tools, you can explain machine learning models globally on all data, or locally on a specific data point using the state-of-art technologies in an easy-to-use and scalable fashion.

## Setup

You are going to work on the Notebook VM you created [earlier](../1-new-workspace/1-setup-compute.md). 

1. To get started, first navigate to the JupyterLab instance running on the Notebook VM by clicking on the JupyterLab link shown below:
![](log_in.png)

1. After going through authentication, you will see the JupyterLab frontend. As you authenticate, make sure to use the same user to log in as was used to create the Notebook VM, or else your access will be denied. Next open an Terminal (either by File/New/Terminal, or by just clicking on Terminal in the Launcher Window).
![](terminal.png)

1. In the terminal window clone this repository by typing:

        git clone https://github.com/danielsc/azureml-workshop-2019

2. After the clone completes, in the file explorer on the left, navigate to the folder `2-interpretability` and open the notebook `1-simple-feature-transformations-explain-local.ipynb`:
![](notebook.png)

Now follow the instructions in the notebook.



