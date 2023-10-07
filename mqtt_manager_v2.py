import json
import datetime
import logging
import paho.mqtt.client as mqtt
from clickhouse_driver import Client as ClickhouseClient
from pymongo import MongoClient

# Constants
CLICKHOUSE_SERVER = "127.0.0.1"
MONGODB_SERVER = "your_mongodb_server"
MONGODB_DATABASE = "your_mongodb_database"
MONGODB_COLLECTION = "your_mongodb_collection"

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def update_clickhouse(data):
    try:
        client = ClickhouseClient(CLICKHOUSE_SERVER)
        query = f"INSERT INTO table1 VALUES (%s, %s, %s, %s, %s)"
        client.execute(query, data)
        logger.debug('Inserted data into ClickHouse: %s', data)
    except Exception as e:
        logger.error('Error inserting data into ClickHouse: %s', e)

def update_mongodb(data):
    try:
        client = MongoClient(MONGODB_SERVER)
        db = client[MONGODB_DATABASE]
        collection = db[MONGODB_COLLECTION]
        collection.insert_one(data)
        logger.debug('Inserted data into MongoDB: %s', data)
    except Exception as e:
        logger.error('Error inserting data into MongoDB: %s', e)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        logger.debug('Received MQTT message: %s', data)

        if data.get('message_type') == 'periodic':
            # Handle periodic data and store in ClickHouse
            timestamp = datetime.datetime.utcfromtimestamp(data.get('ts'))
            user_name = data.get('user_name', '')
            client_name = data.get('client_name', '')
            param_subtree = data.get('param_subtree', {})
            
            for param_name, param_value in param_subtree.items():
                clickhouse_data = [timestamp, user_name, client_name, param_name, param_value]
                update_clickhouse(clickhouse_data)

        elif data.get('message_type') == 'cli_response':
            # Handle CLI response data and store in MongoDB
            user_name = data.get('user_name', '')
            client_name = data.get('client_name', '')
            last_cli_response = data.get('param_subtree', {}).get('cli_response_body', '')
            
            mongo_data = {
                'ts_last_message': datetime.datetime.now(),
                'last_cli_response': last_cli_response
            }
            update_mongodb(mongo_data)

    except Exception as e:
        logger.error('Error processing received MQTT message: %s', e)

# Set up MQTT client
mqttClient = mqtt.Client("collector_client")
mqttClient.on_message = on_message
mqttClient.connect("your_mqtt_broker")
mqttClient.subscribe("your_mqtt_topic")

# Start MQTT client loop
mqttClient.loop_forever()
