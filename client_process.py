import time
from datetime import datetime
import json
import sys
import getopt
import paho.mqtt.client as mqtt
import numpy as np
import logging
import subprocess

# Constants
MQTT_BROKER = "127.0.0.1"
TOPIC_US = 'us_topic_for_all'
SLEEP_INTERVAL = 0.3
COLLECTION_INTERVAL = 3 # in seconds

class MqttClient:
    def __init__(self, user_name, client_name):
        self.user_name = user_name
        self.client_name = client_name
        self.topic_ds = f'{user_name}_{client_name}_ds'
        self.client = None
        self.last_data_sent_time = None

    def create_param_subtree(self):
        param_val1 = str(np.random.normal(20, 5, 1)[0])
        param_val2 = str(np.random.normal(100, 10, 1)[0])
        param_subtree = {'param1': param_val1, 'param2': param_val2}
        return param_subtree

    def mqtt_establish(self):
        client = mqtt.Client(self.client_name)
        client.connect(MQTT_BROKER)
        return client

    def send_data_to_broker(self):
        if self.last_data_sent_time is None or time.time() - self.last_data_sent_time >= COLLECTION_INTERVAL:
            try:
                param_subtree = self.create_param_subtree()
                message = {
                    'ts': time.mktime(datetime.now().timetuple()),
                    'user_name': self.user_name,
                    'client_name': self.client_name,
                    'param_subtree': param_subtree,
                    'message_type': 'periodic',
                }
                res = self.client.publish(TOPIC_US, json.dumps(message))
                self.last_data_sent_time = time.time()
                time.sleep(0.3)
                logging.info('Sending data1 result: %s, message: %s', res.is_published(), message)

            except Exception as e:
                logging.error('An error occurred: %s, skipping this data point...', e)

    def run_cli_command(self, command):
        try:
            # Run the command in the shell, capture the output
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

            # Return the result
            return result.strip()
        except subprocess.CalledProcessError as e:
            # Handle command execution errors
            return f"Error: {e}"

    
    def on_message(self, client, userdata, message_initial):
        message = message_initial.payload.decode()
        message = message.replace("'", "\"")
        message = json.loads(message)
        logging.info('Message received in client: %s', message)
        
        if message['message_type'] == 'cli_request':
            cli_res = self.run_cli_command(message['message_body'])

        response_message = {
            'ts': time.mktime(datetime.now().timetuple()),
            'user_name': self.user_name,
            'client_name': self.client_name,
            'param_subtree': {'cli_response_body': str(cli_res)},
            'message_type': 'cli_response',
        }

        try:
            response = self.client.publish(TOPIC_US, json.dumps(response_message))
            time.sleep(1)
            logging.info('Sending response to the broker: %s', response.is_published())
        except Exception as e:
            logging.error('Error sending response to the broker: %s', e)



    def run(self):
        while True:
            if not self.client:
                try:
                    logging.info('No client is defined, going to create the handler.')
                    self.client = self.mqtt_establish()
                    time.sleep(SLEEP_INTERVAL)
                    self.client.on_message = self.on_message
                    self.client.subscribe(self.topic_ds)
                    logging.info('Just after subscribe')
                    time.sleep(SLEEP_INTERVAL)
                    self.client.loop_start()
                    time.sleep(SLEEP_INTERVAL)
                except Exception as e:
                    logging.error('The initial connection attempt failed, error: %s', e)
                    time.sleep(SLEEP_INTERVAL)
                    continue
            else:
                self.send_data_to_broker()
            time.sleep(SLEEP_INTERVAL)

def get_args(argv):
    arg_user_name = ""
    arg_client_name = ""
    arg_help = f"{argv[0]} -u <user_name> -c <client_name>"

    try:
        opts, args = getopt.getopt(argv[1:], "hu:c:t:", ["help", "user_name=", "client_name="])
    except Exception:
        logging.error("Error parsing command line arguments.")
        print(arg_help)
        sys.exit(1)

    if not opts:
        logging.error("Missing required arguments.")
        print(arg_help)
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)
            sys.exit(1)
        elif opt in ("-u", "--user_name"):
            arg_user_name = arg
        elif opt in ("-c", "--client_name"):
            arg_client_name = arg

    return {'user_name': arg_user_name, 'client_name': arg_client_name}

if __name__ == "__main__":
    commands = get_args(sys.argv)
    user_name = commands['user_name']
    client_name = commands['client_name']

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    mqtt_client = MqttClient(user_name, client_name)
    
    try:
        mqtt_client.run()
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
