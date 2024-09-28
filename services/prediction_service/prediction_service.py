import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
import logging
import random

KAFKA_INPUT_TOPIC = 'iot-data'
KAFKA_OUTPUT_TOPIC = 'predictions'
KAFKA_SERVER = 'localhost:9092'  # Kafka server

logging.basicConfig(level=logging.INFO)

async def predict_traffic(iot_data):
    """Run the ML model to predict if the traffic is crowded."""
    # Simulate ML prediction: return 'Crowded' or 'Not Crowded'
    traffic_condition = random.choice(['Crowded', 'Not Crowded'])
    logging.info(f"Traffic prediction: {traffic_condition}")
    return traffic_condition

async def consume_and_predict():
    consumer = AIOKafkaConsumer(KAFKA_INPUT_TOPIC, bootstrap_servers=KAFKA_SERVER)
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)

    await consumer.start()
    await producer.start()

    try:
        async for msg in consumer:
            iot_data = json.loads(msg.value.decode('utf-8'))
            prediction = await predict_traffic(iot_data['iot_data'])

            # Send the prediction to the E2 Interface service through Kafka
            await producer.send(KAFKA_OUTPUT_TOPIC, json.dumps({'prediction': prediction}).encode('utf-8'))
            logging.info(f"Sent prediction: {prediction} to Kafka topic: {KAFKA_OUTPUT_TOPIC}")
    finally:
        await consumer.stop()
        await producer.stop()

if __name__ == "__main__":
    asyncio.run(consume_and_predict())
