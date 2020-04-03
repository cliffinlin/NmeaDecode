#!/usr/bin/env python
import datetime

DATE_STRING_LENGTH_MIN = 6
DATE_STRING_DAY_INDEX_MIN = 0
DATE_STRING_DAY_INDEX_MAX = 2
DATE_STRING_MONTH_INDEX_MIN = 2
DATE_STRING_MONTH_INDEX_MAX = 4
DATE_STRING_YEAR_INDEX_MIN = 4

TIME_STRING_LENGTH_MIN = 6
TIME_STRING_HOUR_INDEX_MIN = 0
TIME_STRING_HOUR_INDEX_MAX = 2
TIME_STRING_MINUTE_INDEX_MIN = 2
TIME_STRING_MINUTE_INDEX_MAX = 4
TIME_STRING_SECOND_INDEX_MIN = 4

LATITUDE_STRING_LENGTH_MIN = 4
LATITUDE_STRING_DEGREE_INDEX_MIN = 0
LATITUDE_STRING_DEGREE_INDEX_MAX = 2
LATITUDE_STRING_MINUTE_INDEX_MIN = 2

LONGITUDE_STRING_LENGTH_MIN = 5
LONGITUDE_STRING_DEGREE_INDEX_MIN = 0
LONGITUDE_STRING_DEGREE_INDEX_MAX = 3
LONGITUDE_STRING_MINUTE_INDEX_MAX = 3

DEFAULT_ROUND_NDIGITS = 4
SEPARATE_STRING = ",\t"

DEFAULT_TIME_ZONE = 8
DEFAULT_DATE_TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class NmeaSentence:
    def __init__(self):
        self.Separate = SEPARATE_STRING

        # self.LastSentence = ""
        self.Sentence = ""
        self.DataType = ""
        self.Checksum = ""
        self.Data = None

        self.Date = ""
        self.Year = None
        self.Month = None
        self.Day = None

        self.Time = ""
        self.Hour = None
        self.Minute = None
        self.Second = None

        self.Latitude = ""
        self.LatitudeDirection = ""
        self.LatitudeValue = None
        self.Longitude = ""
        self.LongitudeDirection = ""
        self.LongitudeValue = None
        self.Altitude = ""
        self.AltitudeUnit = ""

        self.FixQuality = ""
        self.TrackedNumber = ""

        self.Selection = ""
        self.FixType = ""

        self.View = ""

        self.Used = None

        self.SatelliteList = []

        self.PDOP = ""
        self.HDOP = ""
        self.VDOP = ""

        self.Status = ""

        self.TrueTrack = ""
        self.TrueTrackMark = ""
        self.MagneticTrack = ""
        self.MagneticTrackMark = ""
        self.SpeedN = ""
        self.SpeedNMark = ""
        self.SpeedM = ""
        self.SpeedMMark = ""

        self.GeoidSeparation = ""
        self.GeoidSeparationUnit = ""
        self.DifferentialDataAge = ""
        self.ReferenceStationID = ""

    def reset(self):
        # last_sentence = self.LastSentence
        self.__init__()
        # self.LastSentence = last_sentence

    def decode(self, line):
        self.reset()

        if line is None:
            return

        index = line.find(self.DataType)
        if index == -1:
            return

        nmea_line = line[index:]

        nmea_line = nmea_line.strip()
        if nmea_line is None:
            return

        list_a = nmea_line.split("*")
        if list_a is None:
            return

        if len(list_a) < 2:
            return

        # if nmea_line in self.LastSentence:
            # print("Same sentence found, " + nmea_line +  " " + self.LastSentence)
            # return

        self.Checksum = list_a[1]

        list_b = list_a[0].split(",")
        if list_b is None:
            return

        if len(list_b) < 2:
            return

        self.DataType = list_b[0]
        self.Data = list_b[1:]

        self.Sentence = nmea_line
        # self.LastSentence = self.Sentence

    def decode_date(self):
        if self.Date is None:
            return

        date = self.Date.strip()
        if date is None:
            return
        if len(date) < DATE_STRING_LENGTH_MIN:
            return

        self.Day = date[DATE_STRING_DAY_INDEX_MIN:DATE_STRING_DAY_INDEX_MAX]
        self.Month = date[DATE_STRING_MONTH_INDEX_MIN:DATE_STRING_MONTH_INDEX_MAX]
        self.Year = date[DATE_STRING_YEAR_INDEX_MIN:]

        if len(self.Year) == 2:
            self.Year = "20" + self.Year

    def decode_time(self):
        if self.Time is None:
            return

        time = self.Time.strip()
        if time is None:
            return
        if len(time) < TIME_STRING_LENGTH_MIN:
            return

        self.Hour = time[TIME_STRING_HOUR_INDEX_MIN:TIME_STRING_HOUR_INDEX_MAX]
        self.Minute = time[TIME_STRING_MINUTE_INDEX_MIN:TIME_STRING_MINUTE_INDEX_MAX]
        self.Second = time[TIME_STRING_SECOND_INDEX_MIN:]

    def decode_latitude(self):
        if self.Latitude is None or self.LatitudeDirection is None:
            return

        if len(self.Latitude) < LATITUDE_STRING_LENGTH_MIN:
            return

        degree = self.Latitude[LATITUDE_STRING_DEGREE_INDEX_MIN:LATITUDE_STRING_DEGREE_INDEX_MAX]
        minute = self.Latitude[LATITUDE_STRING_MINUTE_INDEX_MIN:]

        self.LatitudeValue = float(degree) + float(minute) / 60.0

        if self.LatitudeDirection == "S":
            self.LatitudeValue = -1 * self.LatitudeValue

    def decode_longitude(self):
        if self.Longitude is None or self.LongitudeDirection is None:
            return

        if len(self.Longitude) < LONGITUDE_STRING_LENGTH_MIN:
            return

        degree = self.Longitude[LONGITUDE_STRING_DEGREE_INDEX_MIN:LONGITUDE_STRING_DEGREE_INDEX_MAX]
        minute = self.Longitude[LONGITUDE_STRING_MINUTE_INDEX_MAX:]

        self.LongitudeValue = float(degree) + float(minute) / 60.0

        if self.LongitudeDirection == "W":
            self.LongitudeValue = -1 * self.Longitude

    def set_date(self, date, day, month, year):
        self.Date = date
        self.Day = day
        self.Month = month
        self.Year = year

    def set_time(self, time, hour, minute, second):
        self.Time = time
        self.Hour = hour
        self.Minute = minute
        self.Second = second

    def set_latitude(self, latitude, latitudeValue):
        self.Latitude = latitude
        self.LatitudeValue = latitudeValue

    def set_longitude(self, longitude, longitudeValue):
        self.Longitude = longitude
        self.LongitudeValue = longitudeValue

    def set_altitude(self, altitude):
        self.Altitude = altitude

    def set_fix_quality(self, fix_quality):
        self.FixQuality = fix_quality

    def set_tracked_number(self, tracked_number):
        self.TrackedNumber = tracked_number

    def set_speed_n(self, speed_n):
        self.SpeedN = speed_n

    def set_speed_m(self, speed_m):
        self.SpeedM = speed_m

    def set_fix_type(self, fix_type):
        self.FixType = fix_type

    def set_differential_data_age(self, differential_data_age):
        self.DifferentialDataAge = differential_data_age

    def set_reference_station_id(self, reference_station_id):
        self.ReferenceStationID = reference_station_id

    def set_satellite_list(self, satellite_list):
        if satellite_list is None:
            return
        self.SatelliteList = satellite_list

    def set_pdop(self, pdop):
        self.PDOP = pdop

    def set_hdop(self, hdop):
        self.HDOP = hdop

    def set_vdop(self, vdop):
        self.VDOP = vdop

    def get_utc_date_time(self):
        result = None

        if self.Year is None or self.Month is None or self.Day is None or self.Hour is None or self.Minute is None or self.Second is None:
            return result

        result = datetime.datetime.strptime(
            self.Year + "-" + self.Month + "-" + self.Day + " " + self.Hour + ":" + self.Minute + ":" + self.Second,
            DEFAULT_DATE_TIME_FORMAT)

        return result

    def get_local_date_time(self):
        result = None

        utc_date_time = self.get_utc_date_time()

        if utc_date_time is None:
            return result

        result = utc_date_time + datetime.timedelta(hours=DEFAULT_TIME_ZONE)

        return result

    def utc_date_time_to_string(self):
        result = ""

        if self.Year is None or self.Month is None or self.Day is None or self.Hour is None or self.Minute is None or self.Second is None:
            return result

        utc_date_time = self.get_utc_date_time()
        if utc_date_time is None:
            return result

        result += utc_date_time.strftime(DEFAULT_DATE_TIME_FORMAT)
        result += self.Separate

        return result

    def local_date_time_to_string(self):
        result = ""

        local_date_time = self.get_local_date_time()
        if local_date_time is None:
            return result

        result += local_date_time.strftime(DEFAULT_DATE_TIME_FORMAT)
        result += self.Separate

        return result

    def date_to_string(self):
        result = ""

        if self.Year is None or self.Month is None or self.Day is None:
            return result

        result += "Date:"
        result += self.Year + "-" + self.Month + "-" + self.Day
        result += self.Separate

        return result

    def time_to_string(self):
        result = ""

        if self.Hour is None or self.Minute is None or self.Second is None:
            return result

        result += "Time:"
        result += self.Hour + ":" + self.Minute + ":" + self.Second
        result += self.Separate

        return result

    def latitude_to_string(self):
        result = ""

        if self.LatitudeValue is None:
            return result

        result += "Latitude="
        result += str(self.LatitudeValue)
        result += self.Separate

        return result

    def longitude_to_string(self):
        result = ""
        if self.LongitudeValue is None:
            return result

        result += "Longitude="
        result += str(self.LongitudeValue)
        result += self.Separate

        return result

    def altitude_to_string(self):
        result = ""

        if self.Altitude is None or len(self.Altitude) == 0:
            return result

        result += "Altitude="
        result += self.Altitude + self.AltitudeUnit
        result += self.Separate

        return result

    def fix_quality_to_string(self):
        # http://resources.esri.com/help/9.3/arcgismobile/adf/ESRI.ArcGIS.Mobile~ESRI.ArcGIS.Mobile.Gps.GpsFixStatus.html
        #
        # The fix status indicates the type of signal or technique being used by the GPS receiver to determine it’s
        # location. The fix status is important for the GPS consumer, as it indicates the quality of the signal,
        # or the accuracy and reliability of the location being reported. The GPS receiver includes the fix status
        # with the NMEA sentence broadcast to the Mobile SDK. For a better understanding of the GPS technology and
        # terms please review our understanding GPS document. The fix type is determined by the receiver based on
        # number of satellites visible, the type of GPS receiver and the GPS technology being used.
        #
        # INVALIDFIX indicates that there is no satelitte signal being received or there are not enough satelittes
        # available for proper location determination.
        #
        # GPSFix indicates a standard GPS signal, or Standard Positioning Service (SPS) is being used. SPS is the
        # standard specified level of positioning and timing accuracy that is available, without qualification or
        # restrictions, to any user on a continuous worldwide basis. The accuracy of this service will be established
        # by the U.S. Department of Defense based on U.S. security interests.
        #
        # DGPSFix indicates that Differential GPS is being used to proved increased accuracy over SPS. This technique
        # uses a network of fixed ground based reference stations to broadcast the difference between the positions
        # indicated by the satellite systems and the known fixed positions. These stations broadcast the difference
        # between the measured satellite pseudoranges and actual (internally computed) pseudoranges, and receiver
        # stations may correct their pseudoranges by the same amount.
        #
        # PPSFix indicates that Precise Positioning System, encrypted for government use is being used by the
        # receiver. PPS is the most accurate positioning, velocity, and timing information continuously available,
        # worldwide, from the basic GPS. This service will be limited to authorized U.S. and allied Federal
        # Governments; authorized foreign and military users; and eligible civil users. Unauthorized users will be
        # denied access to PPS through the use of cryptography.
        #
        # REAL TIME KINEMATIC (RTK) satellite navigation is a technique used in land survey based on the use of
        # carrier phase measurements of the GPS, GLONASS and/or Galileo signals where a single reference station
        # provides the real-time corrections of even to a centimeter level of accuracy. When referring to GPS in
        # particular, the system is also commonly referred to as Carrier-Phase Enhancement, CPGPS. This GPS technique
        # uses the radio signal (carrier) to refine it location initially calculated using DGPS. The receivers are
        # able to reachy this level of accuracy by performing an initialization, that requires data from at least
        # five common satellites to initialize on-the-fly (in motion) tracking at least four common satellites after
        # initializing.
        #
        # FLOAT REAL TIME KINEMATIC( Float RTK) is very similar to the fixed RTK method of calculating location,
        # but is not as precise, typically around 20 cm to 1 meter accuracy range. This decreased accuracy is offset
        # by increased speed, since the time consuming initializaton phase is skipped.
        #
        # ESTIMATED FIX or Dead reckoning is the determination of a location based on computations of position given
        # an accurately known point of origin and measurements of speed, heading and elapsed time. Dead reckoning
        # coupled with GPS positioning provides a powerful navigation solution. GPS positioning provides highly
        # accurate “points of origin” when exposed to sufficient satellite signal strengths during a trip. Dead
        # reckoning can be used to “fill in the gaps” when there are insufficient GPS signal strength to obtain an
        # accurate position.
        #
        # MANUAL FIX STATUS - indicates that the location has been manually entered into the GPS receiver, and is not
        # based on the sateliite system. This type of fix is useful for entering the coordinates of a known location,
        # that has been previously measured. In this type of GPS fix the location has been input directly into the
        # GPS receiver, which then reports that to the GSPconnection as a NMEA Sentence. If you are manually entering
        # a coordinate location into a ArcGIS Mobile application, you would typically go directely into the GIS
        # database and not though the GPS receiver.
        #
        # SIMULATION MODE This mode is not always called simulation mode on the different models. On the some models
        # it is called "demo mode" or "gps off" while others call it "Use Indoors" or "gps off". Upon entering
        # simulation mode you will find that the gps seems to have a lock on satellites and everything works
        # similarly to the way it works when you actually have a fix. The satellite status page shows that you have a
        # lock on the satellite graphic display and indicates that you are in Simulation mode in the status text
        # field. The rest of the fields in the unit do not show that you are in simulation mode but may have extra
        # commands or other information and may perform differently. For example, the units with object oriented
        # commands add selection capability for speed and track settings so that you can change them on any screen at
        # any time to permit simulating actual movement while using the gps. Menu oriented units set this information
        # on the original simulation mode setup screen so if you wish to change it you need to revisit the setup
        # screen.
        #
        # One of the uses of simulation mode is to allow for route and waypoint maintenance. While you can perform
        # maintenance on a unit that is trying to track satellites you may get "poor gps coverage" because you are
        # using it indoors or other annoying messages. Setting simulation mode avoids these messages and as a bonus
        # saves about 1/2 on the battery consumption since in this mode all of the power is removed from the receiver
        # circuitry.

        result = ""
        remark = ""

        if self.FixQuality is None or len(self.FixQuality) == 0:
            return result

        value = int(self.FixQuality)

        if value == 0:
            remark = "Invalid"
        elif value == 1:
            remark = "SPS"
        elif value == 2:
            remark = "Differential"
        elif value == 3:
            remark = "PPS"
        elif value == 4:
            remark = "RTK Fixed"
        elif value == 5:
            remark = "RTK Float"
        elif value == 6:
            remark = "Estimated"

        if len(remark) == 0:
            return result

        result = "FixQuality:"
        result += remark
        result += self.Separate

        return result

    def tracked_number_to_string(self):
        result = ""

        if len(self.TrackedNumber) == 0:
            return result

        result += "TrackedNumber="
        result += self.TrackedNumber
        result += self.Separate

        return result

    def selection_to_string(self):
        result = ""

        if self.Selection is None or len(self.Selection) == 0:
            return result

        result += "Selection:"
        if "A" in self.Selection:
            result += "Auto"
        elif "M" in self.Selection:
            result += "Manual"

        result += self.Separate

        return result

    def fix_type_to_string(self):
        result = ""

        if self.FixType is None or len(self.FixType) == 0:
            return result

        result += "FixType="

        value = int(self.FixType)
        if value == 1:
            result += "NoFix"
        elif value == 2:
            result += "2D"
        elif value == 3:
            result += "3D"

        result += self.Separate

        return result

    def view_to_string(self):
        result = ""

        if self.View is None or len(self.View) == 0:
            return result

        result += "View="
        result += self.View
        result += self.Separate

        return result

    def used_to_string(self):
        result = ""

        if self.Used is None or len(self.Used) == 0:
            return result

        result += "Used:"

        count = 0
        for prn in self.Used:
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

    def pdop_to_string(self):
        result = ""

        if self.PDOP is None or len(self.PDOP) == 0:
            return result

        result += "PDOP="
        result += self.PDOP
        result += self.Separate

        return result

    def hdop_to_string(self):
        result = ""

        if self.HDOP is None or len(self.HDOP) == 0:
            return result

        result += "HDOP="
        result += self.HDOP
        result += self.Separate

        return result

    def vdop_to_string(self):
        result = ""

        if self.VDOP is None or len(self.VDOP) == 0:
            return result

        result += "VDOP="
        result += self.VDOP
        result += self.Separate

        return result

    def status_to_string(self):
        result = ""

        if self.Status is None or len(self.Status) == 0:
            return result

        result += "Status:"

        if "A" in self.Status:
            result += "Active"
        elif "V" in self.Status:
            result += "Void"

        result += self.Separate

        return result

    def true_track_to_string(self):
        result = ""

        if len(self.TrueTrack) == 0:
            return result

        result += "TrueTrack="
        result += self.TrueTrack
        result += self.Separate

        return result

    def magnetic_track_to_string(self):
        result = ""

        if len(self.MagneticTrack) == 0:
            return result

        result += "MagneticTrack="
        result += self.MagneticTrack
        result += self.Separate

        return result

    def speed_n_to_string(self):
        result = ""

        if self.SpeedN is None or len(self.SpeedN) == 0:
            return result

        result += "Speed="
        result += self.SpeedN + "KN"
        result += self.Separate

        return result

    def speed_m_to_string(self):
        result = ""

        if self.SpeedM is None or len(self.SpeedM) == 0:
            return result

        result += "Speed="
        result += self.SpeedM + "KM"
        result += self.Separate

        return result

    def geoid_separation_to_string(self):
        result = ""

        if self.GeoidSeparation is None or len(self.GeoidSeparation) == 0:
            return result

        if self.GeoidSeparationUnit is None or len(self.GeoidSeparationUnit) == 0:
            return result

        result += "GeoidSeparation="
        result += self.GeoidSeparation + self.GeoidSeparationUnit
        result += self.Separate

        return result

    def differential_data_age_to_string(self):
        result = ""

        if self.DifferentialDataAge is None or len(self.DifferentialDataAge) == 0:
            return result

        result += "DataAge="
        result += self.DifferentialDataAge
        result += self.Separate

        return result

    def reference_station_id_to_string(self):
        result = ""

        if self.ReferenceStationID is None or len(self.ReferenceStationID) == 0:
            return result

        result += "StationID="
        result += self.ReferenceStationID
        result += self.Separate

        return result

    def to_string(self):
        result = ""

        if len(self.Sentence) == 0:
            return result

        # result += self.Sentence + self.Separate
        result += self.DataType + self.Separate

        return result
