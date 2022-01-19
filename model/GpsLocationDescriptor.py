

class GpsLocationDescriptor:

    FILE_LOCATION_PROVIDER = "location_provider_local"
    GPS_LOCATION_PROVIDER = "location_provider_gps"
    NETWORK_LOCATION_PROVIDER = "location_provider_network"

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def altitude(self):
        return self._altitude

    @property
    def provider(self):
        return self._provider

    def __init__(self, latitude, longitude, altitude, provider):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.provider = provider

    @longitude.setter
    def longitude(self, longitude):
        self._longitude = longitude

    @latitude.setter
    def latitude(self, latitude):
        self._latitude = latitude

    @altitude.setter
    def altitude(self, altitude):
        self._altitude = altitude

    @provider.setter
    def provider(self, provider):
        self._provider = provider

    def __str__(self):
        return f"Longitude: {self.longitude} " \
               f"Latitude: {self.latitude} " \
               f"Altitude: {self.altitude} " \
               f"- provider {self.provider}"
