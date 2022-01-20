from abc import ABC, abstractmethod


class ResourceDataListener(ABC):

    @staticmethod
    def onDataChanged(updatedValue):
        return None
