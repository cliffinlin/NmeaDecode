#!/usr/bin/env python


from NmeaSentence import NmeaSentence

SEPARATE_STRING = " "


class NavigateData(NmeaSentence):
    def __init__(self):
        NmeaSentence.__init__(self)

        self.Separate = SEPARATE_STRING

        self.GPSView = ""
        self.BDSView = ""

        self.GPSUsed = None
        self.BDSUsed = None

        self.GPSSatelliteList = []
        self.BDSSatelliteList = []

    def set_gps_view(self, view):
        self.GPSView = view

    def set_bds_view(self, view):
        self.BDSView = view

    def set_used(self, used):
        self.Used = used

    def set_gps_used(self, used):
        self.GPSUsed = used

    def set_bds_used(self, used):
        self.BDSUsed = used

    def set_satellite_list(self, satellite_list):
        if satellite_list is None:
            return
        self.SatelliteList.extend(satellite_list)

    def set_gps_satellite_list(self, satellite_list):
        if satellite_list is None:
            return
        self.GPSSatelliteList.extend(satellite_list)

    def set_bds_satellite_list(self, satellite_list):
        if satellite_list is None:
            return
        self.BDSSatelliteList.extend(satellite_list)

    def gps_view_to_string(self):
        result = ""

        if self.GPSView is None or len(self.GPSView) == 0:
            return result

        result += "GPSView="
        result += self.GPSView
        result += self.Separate

        return result

    def bds_view_to_string(self):
        result = ""

        if self.BDSView is None or len(self.BDSView) == 0:
            return result

        result += "BDSView="
        result += self.BDSView
        result += self.Separate

        return result

    def gps_used_to_string(self):
        result = ""

        if self.GPSUsed is None or len(self.GPSUsed) == 0:
            return result

        result += "GPSUsed:"

        count = 0
        for prn in self.GPSUsed:
            if prn is not None and len(prn) > 0:
                if count == 0:
                    result += "#" + prn
                else:
                    result += "," + "#" + prn
            count += 1

        result += self.Separate

        return result

    def bds_used_to_string(self):
        result = ""

        if self.BDSUsed is None or len(self.BDSUsed) == 0:
            return result

        result += "BDSUsed:"

        count = 0
        for prn in self.BDSUsed:
            if prn is not None and len(prn) > 0:
                if count == 0:
                    result += "#" + prn
                else:
                    result += "," + "#" + prn
            count += 1

        result += self.Separate

        return result

    def satellite_list_to_string(self):
        result = ""

        if self.SatelliteList is None or len(self.SatelliteList) == 0:
            return result

        for satellite in self.SatelliteList:
            if satellite is not None:
                result += satellite.to_string()

        return result

    def gps_satellite_list_to_string(self):
        result = ""

        if self.GPSSatelliteList is None or len(self.GPSSatelliteList) == 0:
            return result

        for satellite in self.GPSSatelliteList:
            if satellite is not None:
                result += satellite.to_string()

        return result

    def bds_satellite_list_to_string(self):
        result = ""

        if self.BDSSatelliteList is None or len(self.BDSSatelliteList) == 0:
            return result

        for satellite in self.BDSSatelliteList:
            if satellite is not None:
                result += satellite.to_string()

        return result

    def to_string(self):
        result = ""

        result += self.local_date_time_to_string()

        result += self.latitude_to_string()
        result += self.longitude_to_string()
        result += self.altitude_to_string()

        result += self.speed_m_to_string()

        result += self.fix_quality_to_string()
        result += self.fix_type_to_string()

        result += self.differential_data_age_to_string()
        result += self.reference_station_id_to_string()

        result += self.pdop_to_string()
        result += self.hdop_to_string()
        result += self.vdop_to_string()

        result += self.tracked_number_to_string()

        result += self.gps_used_to_string()
        result += self.gps_view_to_string()
        result += self.gps_satellite_list_to_string()

        result += self.bds_used_to_string()
        result += self.bds_view_to_string()
        result += self.bds_satellite_list_to_string()

        result += self.used_to_string()
        result += self.view_to_string()
        result += self.satellite_list_to_string()

        return result
