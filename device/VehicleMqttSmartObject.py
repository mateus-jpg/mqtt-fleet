import logging

from resources.GpsGpxSensorResource import GpsGpxSensorResource
from resources.BatterySensorResource import BatterySensorResource
from resources.ResourceDataListener import ResourceDataListener
from resources.SmartObjectResource import SmartObjectResource
from message.TelemetryMessage import TelemetryMessage

import paho.mqtt.client as mqtt


class VehicleMqttSmartObject:
    smartObjectResource: SmartObjectResource
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger('VEHICLE-SMART-OBJECT')
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    fileHandler = logging.FileHandler("Vehicle.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    TELEMETRY_TOPIC = "telemetry"
    EVENT_TOPIC = "event"
    CONTROL_TOPIC = "control"
    COMMON_TOPIC = "command"
    BASIC_TOPIC = "fleet/vehicle"

    def registerToAvailableResource(self):
        try:
            for self.key in self.resourceMap.keys():
                if self.resourceMap[self.key] is not None:
                    self.smartObjectResource = self.resourceMap[self.key]
                    self.logger.info(f"Registering to Resource : {self.smartObjectResource.deviceType}"
                                     f"(ID:{self.smartObjectResource.deviceId})")
                    if self.smartObjectResource.deviceType == GpsGpxSensorResource.RESOURCE_TYPE:
                        resourceDataListener = ResourceDataListener()
                        resourceDataListener.onDataChanged = self._onDataChangedGps
                        self.smartObjectResource.addDataListener(resourceDataListener)
                    if self.smartObjectResource.deviceType == BatterySensorResource.RESOURCE_TYPE:
                        resourceDataListener = ResourceDataListener()
                        resourceDataListener.onDataChanged = self._onDataChangedBattery
                        self.smartObjectResource.addDataListener(resourceDataListener)
        except Exception as e:
            self.logger.error(f"Error Registering to Resources | msg{str(e)}")

    def _onDataChangedBattery(self, resource: SmartObjectResource, updatedValue):
        try:
            self.publishTelemetryData(f"{self.BASIC_TOPIC}/"
                                      f"{self.vehicleId}/"
                                      f"{self.TELEMETRY_TOPIC}/"
                                      f"{resource.deviceType.split(':')[-1]}",
                                      TelemetryMessage(resource.deviceType, f"{updatedValue:.2f}"))
        except Exception as e:
            self.logger.error(f"Error CallBack _onDataChangedBattery | Msg: {str(e)}")

    def _onDataChangedGps(self, resource: SmartObjectResource, updatedValue):
        try:
            self.publishTelemetryData(f"{self.BASIC_TOPIC}/"
                                      f"{self.vehicleId}/"
                                      f"{self.TELEMETRY_TOPIC}/"
                                      f"{resource.deviceType.split(':')[-1]}",
                                      TelemetryMessage(resource.deviceType, updatedValue.toDictSerial()))
        except Exception as e:
            self.logger.error(f"Error CallBack _onDataChangedGps | Msg: {str(e)}")

    def __init__(self, vehicleId, mqttClient, resourceMap):
        self.key = None
        self.vehicleId = vehicleId
        self.mqttClient = mqttClient
        self.resourceMap = resourceMap
        self.logger.info(f"Vehicle Smart Object Correctly created!")

    def start(self):
        try:
            if (self.mqttClient is not None and
                    self.vehicleId is not None and
                    self.resourceMap is not None and len(self.resourceMap) > 0):
                self.logger.info(f"Starting Vehicle Emulator")
                self.registerToAvailableResource()
        except Exception as e:
            self.logger.error(f"Error Starting VehicleSmartObject| msg : {str(e)}")

    def stop(self):
        pass

    def publishTelemetryData(self, topic, telemetryMessage: TelemetryMessage):
        self.logger.info(f"Sending to topic {topic} data: {telemetryMessage} ")
        if self.mqttClient is not None and telemetryMessage is not None and topic is not None:
            try:
                messagePayload = str.encode(telemetryMessage.writeValueAsString())
                self.mqttClient.publish(topic, messagePayload)
            except Exception as e:
                print(f"{str(e)}")
        else:
            self.logger.error("Error: Topic or Msg = None or MqttClient is not Connected")
