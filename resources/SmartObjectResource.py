from abc import ABC, abstractmethod
import logging
from resources.ResourceDataListener import ResourceDataListener


class SmartObjectResource(ABC):
    logger = logging.getLogger('SmartObjectResource')
    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    fileHandler = logging.FileHandler("smartObjectResource.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    @property
    def deviceId(self):
        return self._deviceId

    @property
    def deviceType(self):
        return self._deviceType

    def __init__(self, deviceType, deviceId):
        self.resourceDataListenerList = list()

        self.deviceId = deviceId
        self.deviceType = deviceType

    def addDataListener(self, resourceDataListener):

        if self.resourceDataListenerList is not None:
            self.resourceDataListenerList.append(resourceDataListener)

    def removeDataListener(self, resourceDataListener):
        if (self.resourceDataListenerList is not None) and (
                self.resourceDataListenerList.__contains__(resourceDataListener)):
            self.resourceDataListenerList.remove(resourceDataListener)

    def __str__(self):
        return f"Device Type: {self.deviceType} - ID: {self.deviceId}"

    @deviceId.setter
    def deviceId(self, value):
        self._deviceId = value

    @deviceType.setter
    def deviceType(self, value):
        self._deviceType = value

    @abstractmethod
    def loadUpdatedValue(self):
        pass

    def notifyUpdate(self, updatedValue):
        if self.resourceDataListenerList is not None and len(self.resourceDataListenerList) > 0:
            for resourceDataListener in self.resourceDataListenerList:
                resourceDataListener.onDataChanged(self, updatedValue)
        else:
            logging.error("Empty or None Data Listener !!")
