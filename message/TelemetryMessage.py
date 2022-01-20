from message.GenericMessage import GenericMessage
import time
import json
from model.JSONUtils import JSONUtils as JU

class TelemetryMessage:

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def type(self):
        return self._type

    @property
    def dataValue(self):
        return self._dataValue

    def __init__(self, type, dataValue):
        self.timestamp = round(time.time() * 1000)
        self.type = type
        self.dataValue = dataValue

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @type.setter
    def type(self, type):
        self._type = type

    @dataValue.setter
    def dataValue(self, dataValue):
        self._dataValue = dataValue

    def __str__(self):
        return f"Timestamp: {self.timestamp} " \
               f"Type: {self.type}" \
               f"DataValue: {self.dataValue}"

    def writeValueAsString(self):
        return json.dumps(self.dict_serialize())

    def dict_serialize(self):
        return (dict(
            (i.replace(self.__class__.__name__, '').lstrip("_"), value)
            for i, value in self.__dict__.items()
        ))

