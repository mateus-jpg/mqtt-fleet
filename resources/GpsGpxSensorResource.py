from threading import Event

from gpxpy.gpx import GPX

from model.GpsLocationDescriptor import GpsLocationDescriptor
from resources.ResourceDataListener import ResourceDataListener
from resources.SmartObjectResource import SmartObjectResource
import logging
import uuid
import gpxpy
import gpxpy.gpx
import schedule
import threading
import time
import sys


class GpsGpxSensorResource(SmartObjectResource):
    gpx: GPX
    stop_periodic_event: Event
    RESOURCE_TYPE = "iot:sensor:gps"
    logger = logging.getLogger('GPS_RESOURCE-LOG')
    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    fileHandler = logging.FileHandler("gps.log")
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    GPX_FILE_NAME = "/home/mramos/OneDrive/PROGETTI RANDOM/mqtt/tracks/track.gpx"
    UPDATE_PERIOD = 1
    WAIT_UPDATE_PERIOD = 1

    def loadUpdatedValue(self):
        return self.updatedGpsLocationDescriptor

    def __init__(self, type=RESOURCE_TYPE, id=uuid.uuid1()):
        super().__init__(type, id)
        self.start()

    def start(self):
        try:
            self.updatedGpsLocationDescriptor = GpsLocationDescriptor
            self.gpx = gpxpy.parse(open(self.GPX_FILE_NAME))
            self.wayPointList = self.gpx.tracks[0].segments[0].points
            self.startingPoint = self.wayPointList[0]
            self.logger.info(f"GPX File waypoint correctly loaded ! size: {len(self.wayPointList)}")
            self.wayPointListIterator = iter(self.wayPointList)

            # Start Callback for automatic Start
            self.main()
        except Exception as e:
            self.logger.error("Error starting gpx Resource | Msg: {}".format(str(e)))

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
        self.logger.info("Updating Resource Value")
        return cease_continuous_run

    def updateWayPointValue(self):
        try:
            try:
                self.currentWayPoint = self.wayPointListIterator.__next__()
                """"
                self.logger.info(
                    f"{self.RESOURCE_TYPE} -> "
                    f"Log: {self.currentWayPoint.longitude} "
                    f"Lat: {self.currentWayPoint.latitude}")
                """
                self.updatedGpsLocationDescriptor = GpsLocationDescriptor(self.currentWayPoint.latitude,
                                                                          self.currentWayPoint.longitude,
                                                                          (self.currentWayPoint.elevation
                                                                           if self.currentWayPoint.elevation is not None
                                                                           else 0.0),
                                                                          GpsLocationDescriptor.FILE_LOCATION_PROVIDER)
                self.notifyUpdate(self.updatedGpsLocationDescriptor)
                if self.currentWayPoint == self.startingPoint:
                    self.logger.info("Track came to End - Stopping Service ")
                    self.stop_periodic_event.set()
            except StopIteration:
                self.logger.info("Reversing wayPoint List")
                self.wayPointList.reverse()
                self.wayPointListIterator = iter(self.wayPointList)
                self.logger.info("Iterating backward to GPS Waypoint List ")
        except RecursionError:
            self.logger.warning("Warning: recursion may never end!!")
        except Exception as e:
            self.logger.error(f"Error Updating wayPoint list | msg {str(e)}")

    def onDataChanged(self, resource, updatedValue):
        if resource.deviceId is not None and updatedValue is not None:
            self.logger.info(f"Device: {resource.deviceId} -> New Value Received {updatedValue}")
        else:
            self.logger.error(f"onDataChanged Callback -> None Resource or None updatedValue")

    def main(self):
        self.logger.info(f"New {self.deviceType} "
                         f"with id: {self.deviceId}"
                         f"Resource Created ! ")
        self.currentWayPoint = self.wayPointListIterator.__next__()
        self.logger.info(f"Starting point at "
                         f"Lat:{self.currentWayPoint.latitude} "
                         f"Long: {self.currentWayPoint.longitude}")
        try:
            time.sleep(self.WAIT_UPDATE_PERIOD)
            schedule.every().second.do(self.updateWayPointValue)
            self.stop_periodic_event = self.periodicEventValueUpdateTask()

        except Exception as e:
            self.logger.error("Error executing periodic value | Msg: {}".format(str(e)))

        resourceDataListener = ResourceDataListener()
        resourceDataListener.onDataChanged = self.onDataChanged
        self.addDataListener(resourceDataListener)
