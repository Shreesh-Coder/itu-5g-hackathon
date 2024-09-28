# Use a lightweight base Python image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /services/iot_ingestion

# Copy the service script and requirements file into the container
COPY iot_ingestion.py .
COPY ../../requirements.txt .

# Install any required Python packages
RUN pip install -r requirements.txt

# Command to run the IoT Ingestion service
CMD ["python", "iot_ingestion.py"]
