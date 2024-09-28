import asyncio
from aiokafka import AIOKafkaProducer
import json
import logging

KAFKA_TOPIC = 'iot-data'
KAFKA_SERVER = 'localhost:9092'  # Kafka server

logging.basicConfig(level=logging.INFO)

async def handle_connection(reader, writer):
    """Handles incoming IoT data connections."""
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_SERVER)
    await producer.start()

    try:
        data = await reader.read(1024)
        if data:
            message = data.decode('utf-8')
            logging.info(f"Received data: {message}")
            await producer.send(KAFKA_TOPIC, json.dumps({'iot_data': message}).encode('utf-8'))
            logging.info(f"Sent data to Kafka topic: {KAFKA_TOPIC}")
        else:
            logging.info("No data received, closing connection.")
    finally:
        writer.close()
        await producer.stop()

async def main():
    server = await asyncio.start_server(handle_connection, 'localhost', 5000)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
