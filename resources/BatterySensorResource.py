import threading
import logging
import time

from resources.SmartObjectResource import SmartObjectResource
import uuid
import random
import schedule
from resources.ResourceDataListener import ResourceDataListener

class BatterySensorResource(SmartObjectResource):
    MIN_BATTERY_LEVEL = 50.0
    MAX_BATTERY_LEVEL = 70.0
    MIN_BATTERY_LEVEL_CONSUMPTION = 0.1
    MAX_BATTERY_LEVEL_CONSUMPTION = 1.0
    UPDATE_PERIOD = 5
    WAIT_UPDATE_PERIOD = 5
    RESOURCE_TYPE = "iot:sensor:battery"
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger('BATTERY_RESOURCE-LOG')
    logger.setLevel(logging.DEBUG)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    fileHandler = logging.FileHandler("battery.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    def __init__(self, type=RESOURCE_TYPE, id=uuid.uuid1()):
        super().__init__(type, id)
        self.start()

    def loadUpdatedValue(self):
        return self.updatedBatteryLevel

    def start(self):
        try:
            self.updatedBatteryLevel = self.MIN_BATTERY_LEVEL + random.uniform(0, 1) * (
                    self.MAX_BATTERY_LEVEL - self.MIN_BATTERY_LEVEL)

            #Start Callback for automatic Start
            self.main()
        except Exception as e:
            self.logger.error(f"Error init battery resources {str(e)}")

    def periodicEventValueUpdateTask(self):
        cease_continuous_run = threading.Event()
        self.logger.info("Start period Update with period: {} s".format(self.UPDATE_PERIOD))

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not cease_continuous_run.is_set():
                    schedule.run_pending()
                    time.sleep(self.UPDATE_PERIOD)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return cease_continuous_run

    def updateBatteryValue(self):

        # self.logger.info("Updating Resource Value...")
        self.updatedBatteryLevel = self.updatedBatteryLevel - (
                self.MIN_BATTERY_LEVEL_CONSUMPTION + self.MAX_BATTERY_LEVEL_CONSUMPTION * random.uniform(0, 1))

        if self.updatedBatteryLevel <= 0:

            self.logger.critical("Battery Died!!!")
            self.notifyUpdate(self.updatedBatteryLevel)
            self.stop_periodic_event.set()
        else:
            self.notifyUpdate(self.updatedBatteryLevel)

    def onDataChanged(self, resource, updatedValue):
        if resource.deviceId is not None and updatedValue is not None:
            self.logger.info(f"Device: {resource.deviceId} -> New Battery Level Received {updatedValue}")
        else:
            self.logger.error(f"onDataChanged Callback -> None Resource or None updatedValue")

    def main(self):
        self.logger.info(
            "New {} with id: {} Resource Created ! "
            "Battery level: {}".format(self.deviceType,
                                       self.deviceId,
                                       self.loadUpdatedValue()))
        try:
            time.sleep(self.WAIT_UPDATE_PERIOD)
            schedule.every().second.do(self.updateBatteryValue)
            self.stop_periodic_event = self.periodicEventValueUpdateTask()

        except Exception as e:
            self.logger.error("Error executing periodic value | Msg{}".format(str(e)))

        resourceDataListener = ResourceDataListener()
        resourceDataListener.onDataChanged = self.onDataChanged
        self.addDataListener(resourceDataListener)
