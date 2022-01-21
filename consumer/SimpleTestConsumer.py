import logging
import uuid
import paho.mqtt.client as mqtt


class SimpleTestConsumer:
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
            self.client = mqtt.Client(client_id=self.clientId, clean_session=True)
            self.client.on_message = self.on_message
            self.client.connect(host=self.BROKER_ADDRESS, port=self.BROKER_PORT)
            self.client.subscribe(topic=self.TARGET_TOPIC)
            self.client.on_message = self.on_message
            self.client.loop_forever()
        except Exception as e:
            self.logger.error(f"Error Starting MQTT Simple Consumer | Msg: {str(e)}")
