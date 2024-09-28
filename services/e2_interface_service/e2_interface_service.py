import asyncio
from aiokafka import AIOKafkaConsumer
import logging
import sctp  # SCTP for E2 interface
import socket

KAFKA_TOPIC = 'predictions'
KAFKA_SERVER = 'localhost:9092'
BASE_STATION_ADDRESS = ('localhost', 5001)  # Example address for base station

logging.basicConfig(level=logging.INFO)

async def handle_prediction(prediction):
    """Allocate network slices based on traffic prediction."""
    # SCTP connection to base station (nodeB)
    conn = sctp.sctpsocket_tcp(socket.AF_INET)
    conn.connect(BASE_STATION_ADDRESS)
    
    if prediction == 'Crowded':
        logging.info("Allocating mMTC and URLLC slices (traffic is crowded)")
        conn.send(b'ENABLE_URLLC_SLICE')
        conn.send(b'ENABLE_MMT_C_SLICE')
    else:
        logging.info("Allocating mMTC slice only (traffic is normal)")
        conn.send(b'ENABLE_MMT_C_SLICE')
    
    conn.close()

async def consume_predictions():
    consumer = AIOKafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_SERVER)
    await consumer.start()

    try:
        async for msg in consumer:
            prediction = json.loads(msg.value.decode('utf-8'))['prediction']
            logging.info(f"Received prediction: {prediction}")
            await handle_prediction(prediction)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_predictions())
