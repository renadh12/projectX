# projectX
## End to End Data/ML Engineering Project using PySpark, Kubernetes, Docker and Azure

### Overview:
This project serves as an end-to-end template for Data/ML engineering using PySpark, Docker, and Kubernetes on Azure. It processes datasets, trains and evaluates a PySpark ML Regression model, dockerizes the Python code, and deploys it to an Azure Kubernetes Services (AKS) cluster.

### Key Features:

#### PySpark Data Processing:

- Utilizes PySpark ML features like StringIndexer and VectorAssembler for dataset processing.

#### PySpark Model Training and Evaluation:

- Employs PySpark ML Regression to predict total bills for each customer.
- Evaluates model performance using key metrics: coefficients, intercept, R-squared, Mean Absolute Error, and Mean Squared Error.

#### Dockerization:

- ##### Dockerfile:
  - Reference the provided Dockerfile to create your own to package Python Spark code, any dataset in csv format, and requirements.txt.
- #### Azure Container Registry (ACR):
  - Build and push your Docker image to Azure Container Registry. [Pre-req: Create an account on Azure](https://go.microsoft.com/fwlink/?linkid=2227353&clcid=0x409&l=en-us&srcurl=https%3A%2F%2Fazure.microsoft.com%2Ffree)

#### Deployment using Kubernetes

