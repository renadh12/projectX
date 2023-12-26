# projectX
## End to End Data/ML Engineering Project using PySpark, Kubernetes, Docker and Azure

### Overview:
This project serves as an end-to-end template for Data/ML engineering using PySpark, Docker, and Kubernetes on Azure. The PySpark code processes the datasets, trains and evaluates a Linear Regression model, returns the predicted total bill, coefficients, intercept, R-squared, Mean Absolute Error, and Mean Squared Error. The Python code is dockerized, and deployed to an Azure Kubernetes Services (AKS) cluster.

### Key Features:

#### PySpark Data Processing:

- Utilizes PySpark ML features like StringIndexer and VectorAssembler to process the dataset.

#### PySpark Model Training and Evaluation:

- Employs Linear Regression Model to predict total bills for each customer based on independent features.
- Evaluates model performance using key metrics: coefficients, intercept, R-squared, Mean Absolute Error, and Mean Squared Error.


#### Azure Resource Creation
- ##### Azure Container Registry (ACR):
  - Please sign up for Azure and create the Azure Container Registry resource using the Azure portal or CLI. [Pre-req: Create an account on Azure](https://go.microsoft.com/fwlink/?linkid=2227353&clcid=0x409&l=en-us&srcurl=https%3A%2F%2Fazure.microsoft.com%2Ffree)
- ##### Azure Kubernetes Services Cluster
  -  On Azure CLI or Portal, create a new resource Azure Kubernetes Services cluster
  -  Grab the API Server address from the Kubernetes service page on the portal
  -  Update line 96 in the Python Spark code
 `spark_session = SparkSession.builder.appName("SparkMLPipeline").config("spark.kubernetes.master", "k8s://https:<API-SERVER-ADDRESS>").getOrCreate()` [Note: This needs to be completed before Dockerization step]
    -  This will help Spark to connect to the Kubernetes cluster when it creates a Spark session
  -  Subscribe to the cluster: `az account set --subscription <subscription-id>`
  -  Download cluster credentials: `az aks get-credentials --resource-group <RESOURCE-GROUP-NAME> --name <cluster-name>`

#### Dockerization:

- ##### Dockerfile:
  - Reference the provided Dockerfile to create your own to package Python Spark code, any dataset in csv format, and requirements.txt.
  - Install Docker
  - Log in to your registry
    - `az login`
    - `az acr login --name <container-registry-resource-name>`
    - `docker login`
    - `cd <project-directory>
    - `docker build --no-cache -t <container-registry-resource-name>.azurecr.io/<app-name>:<tag> .`
    - Example: `docker build --no-cache -t kubspark.azurecr.io/spark-app:latest .`
    - `docker push kubspark.azurecr.io/spark-app:latest`

#### Deployment using Kubernetes
- Reference the provided Kubernetes deployment file and only update the values where you see `spark-app` with your specified project name and update the container image name accordingly (`<container-registry-resource-name>.azurecr.io/<app-name>:<tag>`)
- Once the file has been updated, run the following command to deploy your pushed imgage in the container registry to the kubernetes cluster
  - `kubectl apply -f spark-deploy.yml`
 
#### Validation
- Run `kubect get pods` to check the status of the deployment. Status should say Completed
- Copy the `pod_name` [example: `spark-app-67c81231c`]
- Run `kubectl logs <pod_name>` to view the log
- Validate the presence of the predicted total bill, coefficients, intercept, R-squared, Mean Absolute Error, and Mean Squared Error
- This should confirm the end-to-end flow as the Python code is functional inside the Kubernetes cluster

#### Goal

The goal of this project is the work on any given data engineering project, dockerize and deploy it in quick seamless steps. After you're done with the Validation step, you can refactor the Python code, use a different dataset, employ a ML model that serves your requirements and then follow the same exact steps to dockerize and deploy your project to a Kubernetes cluster on Azure.


