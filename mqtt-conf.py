class MqttConf:

    totalTelemetryMessageLimit = 1000
    startUpDelayMs = 5000
    mqttOutgoingClientQoS = 0

    def __init__(self, mqttBrokerAdress,
                 mqttBrokerPort,
                 ):
        self.mqttBrokerPort = mqttBrokerPort
        self.mqttBrokerAdress = mqttBrokerAdress