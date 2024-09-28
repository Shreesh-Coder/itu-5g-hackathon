# 5G-Powered Smart City Transit System

This project simulates a **5G-Powered Smart City Transit System**, consisting of three microservices:
1. **IoT Ingestion Service**: Ingests IoT data from public transportation systems.
2. **Prediction Service**: Analyzes IoT data to predict traffic congestion.
3. **E2 Interface Service**: Manages communication with 5G base stations, handling network slicing for public transport.

The system is containerized using **Docker** and orchestrated using **Kubernetes**. The project uses **Kafka** for message brokering between services and **Zookeeper** for managing Kafka clusters.

---

## **Project Structure**

```
5G HACKATHON/
│
├── deployments/                          # Kubernetes deployment files
│   ├── e2-interface-deployment.yaml      # Deployment file for E2 Interface Service
│   ├── iot-ingestion-deployment.yaml     # Deployment file for IoT Ingestion Service
│   └── prediction-service-deployment.yaml # Deployment file for Prediction Service
│
├── services/                             # Service code and Dockerfiles
│   ├── e2_interface_service/
│   │   ├── e2_interface_service.py       # E2 Interface Service code
│   │   └── Dockerfile                    # Dockerfile for E2 Interface Service
│   ├── iot_ingestion/
│   │   ├── iot_ingestion.py              # IoT Ingestion Service code
│   │   └── Dockerfile                    # Dockerfile for IoT Ingestion Service
│   └── prediction_service/
│       ├── prediction_service.py         # Prediction Service code
│       └── Dockerfile                    # Dockerfile for Prediction Service
│
├── docker-compose.yml                    # Docker Compose configuration for Kafka & services
├── requirements.txt                      # Common dependencies for all services
└── README.md                             # Project documentation
```

---

## **Flow of the Code**

### 1. **IoT Ingestion Service** (`iot_ingestion.py`)
   - This service collects real-time location and capacity data from IoT devices (like buses, trains, and metro systems).
   - Data is then sent to **Kafka** for further processing.
   - The service is exposed externally using **NodePort**.

### 2. **Prediction Service** (`prediction_service.py`)
   - The Prediction Service consumes data from Kafka and uses a machine learning model to predict whether the traffic is **crowded** or **not crowded**.
   - Once a prediction is made, it is sent back to Kafka for further use by the E2 Interface Service.

### 3. **E2 Interface Service** (`e2_interface_service.py`)
   - The E2 Interface Service consumes the prediction data from Kafka.
   - Based on the predictions, the service communicates with the 5G base station to manage network slices using **mMTC** and **URLLC** technologies. 
   - If traffic is **crowded**, it allocates high-priority slices like URLLC; if **not crowded**, it only uses mMTC.

---

## **How to Run the Code**

### **Step 1: Clone the Repository**

Clone this repository to your local machine:

```bash
git clone https://github.com/your-repository/itu-5g-hackathon.git
cd itu-5g-hackathon
```

### **Step 2: Build Docker Images**

You need to build Docker images for each service (IoT Ingestion, Prediction, E2 Interface). Each service has its own Dockerfile located in its respective directory.

1. **Build IoT Ingestion Service**:

   ```bash
   docker build -t your-dockerhub/iot-ingestion:latest -f services/iot_ingestion/Dockerfile .
   ```

2. **Build Prediction Service**:

   ```bash
   docker build -t your-dockerhub/prediction-service:latest -f services/prediction_service/Dockerfile .
   ```

3. **Build E2 Interface Service**:

   ```bash
   docker build -t your-dockerhub/e2-interface-service:latest -f services/e2_interface_service/Dockerfile .
   ```

### **Step 3: Push Docker Images to Docker Hub**

Push each service's Docker image to your Docker Hub account:

1. **Push IoT Ingestion Image**:

   ```bash
   docker push your-dockerhub/iot-ingestion:latest
   ```

2. **Push Prediction Service Image**:

   ```bash
   docker push your-dockerhub/prediction-service:latest
   ```

3. **Push E2 Interface Service Image**:

   ```bash
   docker push your-dockerhub/e2-interface-service:latest
   ```

### **Step 4: Start Kafka and Zookeeper**

Use the **Docker Compose** file to bring up Kafka and Zookeeper:

```bash
docker-compose up
```

This will start Kafka and Zookeeper, which are needed for message brokering between the services.

### **Step 5: Deploy Services to Kubernetes**

Once you have the Docker images ready, apply the Kubernetes deployment files for each service.

1. **Deploy IoT Ingestion Service**:

   ```bash
   kubectl apply -f deployments/iot-ingestion-deployment.yaml
   ```

2. **Deploy Prediction Service**:

   ```bash
   kubectl apply -f deployments/prediction-service-deployment.yaml
   ```

3. **Deploy E2 Interface Service**:

   ```bash
   kubectl apply -f deployments/e2-interface-deployment.yaml
   ```

### **Step 6: Access the IoT Ingestion Service**

Since the **IoT Ingestion Service** is exposed using **NodePort**, you can access it using the external IP of your Kubernetes node and the **NodePort** (30001 in this case).

To get the external IP:

```bash
kubectl get nodes -o wide
```

Then access the service at:

```
http://<node-external-ip>:30001
```

### **Step 7: Verify Communication Between Services**

Once deployed, the services will communicate via **Kafka**:
- **IoT Ingestion Service** will send data to Kafka.
- **Prediction Service** will consume data from Kafka, run predictions, and send results back.
- **E2 Interface Service** will consume the prediction results and communicate with the 5G base station to allocate network slices accordingly.

---

### **Common Commands**

- **Check Logs for a Specific Service**:
  ```bash
  kubectl logs <pod-name> -f
  ```

- **Scale Up or Down a Service**:
  ```bash
  kubectl scale deployment <deployment-name> --replicas=<number>
  ```

---

### **Conclusion**

This project simulates how a **5G-powered smart city transit system** can handle public transportation data, predict traffic congestion, and dynamically manage network resources using advanced 5G technologies such as **mMTC** and **URLLC**.

For any issues or further clarifications, please refer to the documentation or reach out to the project contributors.
