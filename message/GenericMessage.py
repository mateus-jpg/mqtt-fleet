from abc import ABC
import json
import time


class GenericMessage(ABC):

    @property
    def type(self):
        return self._type

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def metadata(self):
        return self._metadata

    def __init__(self, type, metadata):
        self.type = type
        self.timestamp = round(time.time() * 1000)
        self.metadata = metadata

    @type.setter
    def type(self, type):
        self._type = type

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @metadata.setter
    def metadata(self, metadata):
        self._metadata = metadata

    def __str__(self):
        return f"Timestamp: {self.timestamp}" \
               f"Type: {self.type}" \
               f"Metadata: {self.metadata}"

    def writeValueAsString(self):
        return json.dumps(self.dict_serialize())

    def dict_serialize(self):
        return (dict(
            (i.replace(self.__class__.__name__, '').lstrip("_"), value)
            for i, value in self.__dict__.items()
        ))
