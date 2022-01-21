import logging
import uuid
import paho.mqtt.client as mqtt
import json
from message.ControlMessage import ControlMessage


class BatteryMonitoringConsumer:
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger("SIMPLE-TEST-CONSUMER")
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    fileHandler = logging.FileHandler("Consumer.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    ALARM_BATTERY_LEVEL = 2.0
    BROKER_ADDRESS = "127.0.0.1"
    BROKER_PORT = 1883
    TARGET_TOPIC = "fleet/vehicle/+/telemetry/battery"
    CONTROL_TOPIC = "control"
    ALARM_MESSAGE_CONTROL_TYE = "battery_alarm_message"
    battery_history_map = dict()
    isAlarmNotified = False

    def on_message(self, client, userdata, msg):
        try:
            self.logger.info(f"Message Received -> Topic{msg.topic} -> Payload : {str(msg.payload)}")
            payload = json.loads(msg.payload)
            if not self.battery_history_map.__contains__(msg.topic):
                self.logger.info(f"Ner Battery Leve saved for {msg.topic}")
                self.battery_history_map[msg.topic] = float(payload['dataValue'])
                self.isAlarmNotified = False
            if self.isBatteryLevelAlarm(self.battery_history_map[msg.topic],
                                        float(payload['dataValue'])) and not self.isAlarmNotified:
                self.logger.info("BATTERY LEVEL ALARM DETECTED! Sending Control Notification")
                self.isAlarmNotified = True

                # incoming topic fleet/vehicle/4adbb940-7ace-11ec-a820-5ff5fbc104a7/telemetry/battery
                controlTopic = f"{msg.topic.replace('telemetry/battery', self.CONTROL_TOPIC)}"
                self.publishControlMessage(controlTopic, ControlMessage(self.ALARM_MESSAGE_CONTROL_TYE,
                                                                        {"charging_station_id": "cs0001",
                                                                         "charging_station_lat": "44.79445705",
                                                                         "charging_station_lon": "10.32004323333333"}))
        except Exception as e:
            self.logger.error(f"Error on_message Callback | Msg: {str(e)}")

    def isBatteryLevelAlarm(self, originalValue, newValue):
        if originalValue - newValue >= self.ALARM_BATTERY_LEVEL:
            return True
        else:
            return False

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

    def publishControlMessage(self, topic, controlMessage: ControlMessage):
        self.logger.info(f"Sending to topic {topic} data: {controlMessage} ")
        if self.client is not None and controlMessage is not None and topic is not None:
            try:
                messagePayload = str.encode(controlMessage.writeValueAsString())
                self.client.publish(topic, messagePayload)
                self.logger.info("Message Correctly published")
            except Exception as e:
                print(f"{str(e)}")
        else:
            self.logger.error("Error: Topic or Msg = None or MqttClient is not Connected")
