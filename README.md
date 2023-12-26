# projectX
## End to End Data/ML Engineering Project using PySpark, Kubernetes, Docker and Azure

Overview:
This project serves as an end-to-end template for Data/ML engineering using PySpark, Docker, and Kubernetes on Azure. It processes datasets, trains and evaluates a PySpark ML Regression model, dockerizes the Python code, and deploys it to an Azure Kubernetes Services (AKS) cluster.

Key Features:

Data Processing:

Utilizes PySpark ML features like StringIndexer and VectorAssembler for dataset processing.
Model Training and Evaluation:

Employs PySpark ML Regression to predict total bills.
Evaluates model performance using key metrics: coefficients, intercept, R-squared, Mean Absolute Error, and Mean Squared Error.
Dockerization:

Dockerfile:
Creates a Dockerfile for packaging Python code, tips.csv dataset, and requirements.txt.
Azure Container Registry (ACR):
Builds and pushes the Docker image to Azure Container Registry.
