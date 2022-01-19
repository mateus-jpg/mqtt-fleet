import uuid

import paho.mqtt.client as mqtt

from device.VehicleMqttSmartObject import VehicleMqttSmartObject
from resources.BatterySensorResource import BatterySensorResource
from resources.GpsGpxSensorResource import GpsGpxSensorResource
import logging


class VehicleSmartObjectProcess:
    logger = logging.getLogger('VehicleProcess')
    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    fileHandler = logging.FileHandler("vehicleProcess.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    MQTT_BROKER_IP = "127.0.0.1"
    MQTT_BROKER_PORT = 1883

    def __init__(self):
        try:

            # generazione uuid
            self.vehicleId = uuid.uuid1().__str__()
            self.resourceMap = dict()
            self.resourceMap = {
                "gps": GpsGpxSensorResource(),
                "battery": BatterySensorResource()
            }

            self.mqttClient = mqtt.Client(self.vehicleId, clean_session=True)
            self.mqttClient.connect(self.MQTT_BROKER_IP, self.MQTT_BROKER_PORT, keepalive=10)
            self.logger.info(f"MQTT Client Connected! ClientId: {self.vehicleId}")
            self.vehicleMqttSmartObject = VehicleMqttSmartObject(self.vehicleId, self.mqttClient, self.resourceMap)
            self.vehicleMqttSmartObject.start()
        except Exception as e:
            self.logger.error(f"Error Initializing Vehicle Process | Msg: {str(e)}")
