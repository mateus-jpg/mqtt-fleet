import logging
import uuid
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as mqtt
import json


class SimpleTestConsumer:
    with open('json_data.json') as json_file:
        config = json.load(json_file)

    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger("SIMPLE-TEST-CONSUMER")
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    fileHandler = logging.FileHandler("Consumer.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    BROKER_ADDRESS = "127.0.0.1"
    BROKER_PORT = 1883
    TARGET_TOPIC = "#"

    def on_message(self, client, userdata, msg):
        self.logger.info(f"Message Received -> Topic{msg.topic} -> Payload : {str(msg.payload)}")

    def __init__(self):
        self.logger.info("MQTT Consumer Test Started")
        try:
            self.clientId = str(uuid.uuid1())
            self.client = mqtt(self.clientId)
            self.client.configureEndpoint(self.config['host'], int(self.config['port']))
            self.client.configureCredentials(self.config['RootCA'],
                                             self.config['PrivateKey'],
                                             self.config['Certificate'])
            self.client.configureAutoReconnectBackoffTime(1, 32, 20)
            self.client.configureOfflinePublishQueueing(-1)
            self.client.configureDrainingFrequency(2)
            self.client.configureConnectDisconnectTimeout(10)
            self.client.configureMQTTOperationTimeout(5)
            self.client.connect()
            self.client.subscribe(self.TARGET_TOPIC, 0, self.on_message)
        except Exception as e:
            self.logger.error(f"Error Starting MQTT Simple Consumer | Msg: {str(e)}")
