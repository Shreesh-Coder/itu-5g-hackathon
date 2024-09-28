# Use a lightweight base Python image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /services/e2_interface_service

# Copy the service script and requirements file into the container
COPY e2_interface_service.py .
COPY ../../requirements.txt .

# Install any required Python packages
RUN pip install -r requirements.txt

# Command to run the E2 Interface Service
CMD ["python", "e2_interface_service.py"]
