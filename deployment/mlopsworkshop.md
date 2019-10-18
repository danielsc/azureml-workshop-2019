
Automating Training
===================

The first phase of bringing your ML workflow to production is being able
to reproduce and automate the model training process.

Azure Machine Learning provides a technology called Machine Learning
pipelines which enables you to define your training workflow in reusable
steps and publish these steps as a Pipeline Endpoint which can be
triggered to run on demand, on a time-based schedule, or as new data
becomes available.

Create an ML pipeline from a YML file
=====================================

Automation is easier to create and manage when you use a declarative
format such as YML. Here is an example Azure ML pipeline YML file which
turns the same code you ran earlier into a repeatable pipeline:

```
pipeline:
name: SamplePipelineForTraining
default\_compute: cpu
steps:
TrainStep:
python\_script\_step:
name: "PythonScriptStep"
script\_name: "train\_explain.py"
allow\_reuse: True
source\_directory: "."
runconfig: 'train.runconfig'
outputs:
result:
destination: Output
datastore: workspaceblobstore
type: mount

```

You’ll note this example looks similar to the logic expressed in the
Jupyter notebook, but expressed in an easier to parse and compare
fashion.

To create the ML pipeline, you can run the following command from your
notebook:

**pipeline** = Pipeline.load\_yaml(ws, 'training-pipeline.yml')\
**endpoint** = pipeline.publish('Train IBM Employee Attrition')

Run a Published Pipeline on Demand
==================================

You can run a published pipeline from the SDK / CLI / UI.

Published pipelines can be found in the Endpoints area – click into
Pipeline Endpoints.

![](media/image1.png)

Schedule Experiments to Run Whenever Code is Checked in to Git
==============================================================

To set up automatic experiment submission on Git commits, we are going
to use an Azure DevOps pipeline. The MLOps workshop contains a
predefined pipeline to execute your experiment run & publish your
experiment run as a repeatable pipeline.

To create a DevOps pipeline, navigate to the Pipelines area and click
“new pipeline” (top right)

![](media/image2.png)

Select your repository & then select “Existing Azure Pipelines YML file”

![](media/image3.png)

![](media/image4.png)
![](media/image5.png)

Once this is set up, you can hit “Run” on the pipeline, which will go
execute your experiment.

The DevOps pipeline YML is doing 3 things:

Installing the CLI & attaching to the ML workspace\
'az ml folder attach -w build-2019-demo -g scottgu-all-hands'

Executing your ML experiment as a script run.\
'az ml run submit-script -c train -e test train\_explain.py'

Publishing your ML experiment as a reusable pipeline.\
'az ml pipeline create --name trainattrition -y
training-ml-pipeline.yml'

Automating Deployment
=====================

Model deployment is typically configured to create a pipeline which
enables models to make predictions in real-time or in batch.

In this walkthrough, we will show you how to leverage Azure Machine
Learning + Azure DevOps to deploy a model as a REST API.

Import github repo
==================

![](media/image6.png)
=====================================================================================

Create new release pipeline
===========================

![](media/image7.png)

Add code artifact
=================

![](media/image8.png)

Add model artifact
==================

![](media/image9.png){width="4.537798556430446in"
height="3.7708333333333335in"}

Add deploy task
===============

![](media/image10.png)

Configure deploy task
=====================

![](media/image11.png)

Clone to PROD stage
===================

![](media/image12.png)

Configure gates
===============

![](media/image13.png)

Change name of PROD service
===========================

![](media/image14.png)

Create release!
===============

![](media/image15.png)
