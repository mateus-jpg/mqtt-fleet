import time
import uuid
from device.VehicleMqttSmartObject import VehicleMqttSmartObject
from resources.BatterySensorResource import BatterySensorResource
from resources.GpsGpxSensorResource import GpsGpxSensorResource
import logging
import json
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder


class VehicleSmartObjectProcess:
    with open('json_data.json') as json_file:
        config = json.load(json_file)

    privateKeyPath = "certificates/fa6eaeaf26d6b7648143f45619e0fc0c9b66f27a6643d6b8206a2d6353f976e0-private.pem.key"
    certPath = "certificates/fa6eaeaf26d6b7648143f45619e0fc0c9b66f27a6643d6b8206a2d6353f976e0-certificate.pem.crt"
    endpoint = "avf6pqezt597s-ats.iot.eu-central-1.amazonaws.com"  # eu-central1 (frankfurt)
                # endpoint="avf6pqezt597s-ats.iot.eu-west-3.amazonaws.com"
    caPath = "certificates/AmazonRootCA1.pem"
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

            event_loop_group = io.EventLoopGroup(3)
            host_resolver = io.DefaultHostResolver(event_loop_group)
            client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
            try:
                """"
                self.mqttClient = mqtt(clientID=self.vehicleId)
                self.mqttClient.configureEndpoint(hostName="avf6pqezt597s-ats.iot.eu-west-3.amazonaws.com",
                                                  portNumber=1883)
                self.mqttClient.configureCredentials(CAFilePath="certificates/AmazonRootCA1.pem",
                                                     KeyPath="certificates/private.pem.key",
                                                     CertificatePath="certificates/certificate.pem.crt")

                self.mqttClient.configureAutoReconnectBackoffTime(1, 32, 20)
                self.mqttClient.configureOfflinePublishQueueing(-1)
                self.mqttClient.configureDrainingFrequency(2)
                """
                self.mqttClient = mqtt_connection_builder.mtls_from_path(
                    endpoint=self.endpoint,
                    port=8883,
                    cert_filepath=self.certPath,
                    pri_key_filepath=self.privateKeyPath,
                    client_bootstrap=client_bootstrap,
                    ca_filepath=self.caPath,
                    client_id=f"test-{self.vehicleId}",
                    clean_session=True,
                    tcp_keep_alive=True,
                    tcp_keep_alive_interval_secs=100,
                    tcp_keep_alive_timeout_secs=10,
                    tcp_keep_alive_max_probes=2)

            except Exception as e:
                self.logger.error(f"Error Setup Aws Connection| msg: {str(e)}")
            self.logger.info(f"Connecting...")
            future_connection = self.mqttClient.connect()
            future_connection.result()
            self.resourceMap = {
                "gps": GpsGpxSensorResource(),
                "battery": BatterySensorResource()
            }
            self.logger.info(f"MQTT Client Connected! ClientId: {self.vehicleId}")

            self.vehicleMqttSmartObject = VehicleMqttSmartObject(self.vehicleId, self.mqttClient, self.resourceMap)
            self.vehicleMqttSmartObject.start()
        except Exception as e:
            self.logger.error(f"Error Initializing Vehicle Process | Msg: {str(e)}")
