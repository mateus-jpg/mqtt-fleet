import json

from message.GenericMessage import GenericMessage


class ControlMessage(GenericMessage):

    def __init__(self, type, metadata):
        super().__init__(type, metadata)

    def __str__(self):
        return super().__str__()

    def writeValueAsString(self):
        return json.dumps(self.dict_serialize())

    def dict_serialize(self):
        return (dict(
            (i.replace(self.__class__.__name__, '').lstrip("_"), value)
            for i, value in self.__dict__.items()
        ))

