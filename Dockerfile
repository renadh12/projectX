FROM openjdk:8-jre-slim

# Set the working directory
WORKDIR /app

COPY tips.csv /app/

RUN apt-get update && apt-get install -y python3 python3-pip

# Copy your Python script and dependencies
COPY pyspark_POC.py requirements.txt /app/

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the command to run your script
CMD ["python3", "pyspark_POC.py"]`                                               