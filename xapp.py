import random
import time
import logging
import socket
import json
import sctp  # SCTP for E2 interface
import signal

class SmartCityTransitXApp:
    def __init__(self, model, host='localhost', port=5000):
        self.model = model  # ML model for predicting traffic congestion
        self.host = host
        self.port = port
        self.server = None
        self.conn = None
        self.e2_server = None  # For the E2 interface setup
        self.e2_conn = None  # E2 connection object for base station
        self.current_data = None
        self.start_time = time.time()

        # Network slice commands for mMTC and URLLC
        self.cmds = {
            'ENABLE_URLLC_SLICE': b'ENABLE_URLLC_SLICE',
            'ENABLE_MMT_C_SLICE': b'ENABLE_MMT_C_SLICE',
            'DISABLE_URLLC_SLICE': b'DISABLE_URLLC_SLICE'
        }

        # Handle KeyboardInterrupt for graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)

    def init_e2(self):
        """Initialize the E2 interface to communicate with the base station (nodeB)."""
        try:
            ip_addr = socket.gethostbyname(socket.gethostname())
            port = 5001

            # Start the SCTP server and bind to the address and port for E2 communication
            self.e2_server = sctp.sctpsocket_tcp(socket.AF_INET)
            self.e2_server.bind((ip_addr, port))
            self.e2_server.listen()
            logging.info(f"E2 interface initialized at {ip_addr}:{port}")
        except Exception as e:
            logging.error(f"Error initializing E2 interface: {e}")
            raise

    def init_connection(self):
        """Initialize the connection to receive data from IoT devices."""
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen()
            logging.info(f"Listening on {self.host}:{self.port}")
        except OSError as e:
            logging.error(f"Failed to initialize IoT connection: {e}")
            raise

    def receive_data(self):
        """Receive IoT data from the transportation system."""
        try:
            self.conn, addr = self.server.accept()
            logging.info(f"Connected by {addr}")

            while True:
                try:
                    data = self.conn.recv(1024)
                    if not data:
                        logging.info("No data received, closing connection.")
                        break  # Break loop when no data is received, close the connection

                    logging.info(f"Received data: {data}")
                    self.current_data = data
                    processed_data = self.preprocess_data(data)
                    if processed_data is not None:
                        prediction = self.predict_traffic(processed_data)

                        # Handle prediction result: Allocate slices based on congestion prediction
                        if prediction == 'Crowded':
                            self.allocate_slices(urllc=True)  # Use URLLC and mMTC
                        else:
                            self.allocate_slices(urllc=False)  # Only use mMTC
                    else:
                        logging.error("Failed to preprocess IoT data.")
                except socket.error as e:
                    logging.error(f"Error receiving data from IoT device: {e}")
                    break  # Break loop and close connection on socket error
        except Exception as e:
            logging.error(f"Error accepting IoT connection: {e}")
            raise

    def preprocess_data(self, data):
        """Preprocess the received IoT data."""
        try:
            data_json = json.loads(data.decode('utf-8'))
            location = data_json.get("location")
            capacity = data_json.get("capacity")
            if location is not None and capacity is not None:
                return {"location": location, "capacity": capacity}
            else:
                logging.error("Invalid IoT data format.")
                return None
        except json.JSONDecodeError as e:
            logging.error(f"Failed to decode JSON: {e}")
            return None

    def predict_traffic(self, processed_data):
        """Run the ML model to predict if the traffic is crowded."""
        try:
            if not processed_data:
                return 'Not Crowded'

            # Simulate ML prediction: return 'Crowded' or 'Not Crowded'
            # Replace this with actual model inference
            traffic_condition = random.choice(['Crowded', 'Not Crowded'])
            logging.info(f"Traffic prediction: {traffic_condition}")
            return traffic_condition
        except Exception as e:
            logging.error(f"Error in traffic prediction: {e}")
            return 'Not Crowded'

    def allocate_slices(self, urllc=False):
        """Allocate mMTC and URLLC slices based on traffic prediction."""
        try:
            # Setup connection with base station (nodeB)
            if self.e2_conn is None:
                self.e2_conn, addr = self.e2_server.accept()
                logging.info(f"Connected to base station at {addr}")

            # Allocate resources based on the prediction
            if urllc:
                logging.info("Traffic is crowded. Allocating mMTC and URLLC slices.")
                self.e2_conn.send(self.cmds['ENABLE_URLLC_SLICE'])  # Send command to enable URLLC
                self.e2_conn.send(self.cmds['ENABLE_MMT_C_SLICE'])   # Send command to enable mMTC
            else:
                logging.info("Traffic is normal. Allocating mMTC slice only.")
                self.e2_conn.send(self.cmds['ENABLE_MMT_C_SLICE'])  # Send command to enable only mMTC
        except socket.error as e:
            logging.error(f"Error sending slice allocation command: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during slice allocation: {e}")

    def shutdown(self, signum, frame):
        """Handle graceful shutdown of sockets on KeyboardInterrupt."""
        logging.info("Shutting down gracefully...")
        if self.conn:
            self.conn.close()
            logging.info("Closed IoT connection.")
        if self.e2_conn:
            self.e2_conn.close()
            logging.info("Closed E2 connection.")
        if self.server:
            self.server.close()
            logging.info("Closed IoT server socket.")
        if self.e2_server:
            self.e2_server.close()
            logging.info("Closed E2 server socket.")
        logging.info("Shutdown complete. Exiting application.")
        exit(0)  # Exit gracefully

    def run(self):
        """Main loop to initialize and run the xApp."""
        try:
            # Initialize both E2 interface and data receiving connections
            self.init_e2()
            self.init_connection()

            while True:
                self.receive_data()
                time.sleep(1)
        except Exception as e:
            logging.error(f"Critical error in xApp execution: {e}")
        finally:
            self.shutdown(None, None)  # Ensure graceful shutdown in case of unhandled errors


# Main execution
if __name__ == "__main__":
    # Initialize your ML model here (placeholder for now)
    dummy_model = None  # Replace with actual model loading logic
    logging.basicConfig(level=logging.INFO)  # Set logging level
    xapp = SmartCityTransitXApp(model=dummy_model)
    xapp.run()
