#!/usr/bin/env python
import folium

import Transform
from BaseMap import BaseMap

GOOGLE_MAP = False

DOP_THRESH_HOLD = 5.0

MAP_DRAW_LINE = True

MAP_DRAW_MARK = True
MAP_DRAW_MARK_COLOR_PDOP = True
MAP_DRAW_MARK_COLOR_FIX_QUALITY = True

MAP_DRAW_MARK_DURATION_IN_SECOND = 10


class FoliumMap(BaseMap):
    def __init__(self):
        BaseMap.__init__(self)

        self.LastDateTime = None

        if GOOGLE_MAP:
            tiles = 'https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}' # google 卫星图
        else:
            tiles = 'http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}'  # 高德卫星图

        self.Map = folium.Map(
            location=self.CenterLocation,
            zoom_start=self.Zoom,
            tiles = tiles,
            # tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}', # 高德街道图
            # tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', # 高德卫星图
            # tiles='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', # google 卫星图
            # tiles='https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}', # google 地图
            attr='default'
        )
        self.Map.add_child(folium.LatLngPopup())

        self.MarkColor = None

    def check_mark_duration(self, navigate_data):
        result = False

        if navigate_data is None:
            return result

        date_time_now = navigate_data.get_local_date_time()
        if date_time_now is None:
            return result

        if self.LastDateTime is not None:
            duration = date_time_now - self.LastDateTime
            if duration.seconds < MAP_DRAW_MARK_DURATION_IN_SECOND:
                return result

        result = True
        self.LastDateTime = date_time_now

        return result

    def set_mark_color(self, navigate_data):
        self.MarkColor = None

        if navigate_data is None:
            return

        if MAP_DRAW_MARK_COLOR_FIX_QUALITY:
            if navigate_data.FixQuality is None or len(navigate_data.FixQuality) == 0:
                return

            value = int(navigate_data.FixQuality)

            if value == 0:
                self.MarkColor = "gray"  # remark = "Invalid"
            elif value == 1:
                self.MarkColor = "blue"  # remark = "SPS"
            elif value == 2:
                self.MarkColor = "lightgreen"  # remark = "DGPS"
            elif value == 3:
                self.MarkColor = "lightgreen"  # remark = "PPS"
            elif value == 4:
                self.MarkColor = "darkgreen"  # remark = "RTK FIX"
            elif value == 5:
                self.MarkColor = "green"  # remark = "RTK Float"
            elif value == 6:
                self.MarkColor = "white"  # remark = "Estimated"

        if MAP_DRAW_MARK_COLOR_PDOP:
            if navigate_data.PDOP is None or len(navigate_data.PDOP) == 0:
                return

            if float(navigate_data.PDOP) > DOP_THRESH_HOLD:
                self.MarkColor = "red"

    def draw(self):
        print("\n")
        print("Prepare data to draw...")
        if self.NavigateDataList is None or len(self.NavigateDataList) == 0:
            print("No data to draw!")
            return

        location_list = []
        for navigate_data in self.NavigateDataList:
            if navigate_data is None:
                continue

            if navigate_data.LatitudeValue is None or navigate_data.LongitudeValue is None:
                continue

            # print("navigate_data=" + navigate_data.to_string())

            mglng, mglat = Transform.wgs84_to_gcj02(navigate_data.LongitudeValue, navigate_data.LatitudeValue)

            if GOOGLE_MAP:
                location = [navigate_data.LatitudeValue, navigate_data.LongitudeValue]
            else:
                location = [mglat, mglng]

            location_list.append(location)

            if MAP_DRAW_MARK:
                if self.check_mark_duration(navigate_data):
                    popup = navigate_data.to_string()

                    self.set_mark_color(navigate_data)

                    if self.MarkColor is not None:
                        folium.Marker(location=location, popup=popup, icon=folium.Icon(color=self.MarkColor)).add_to(
                            self.Map)
                    else:
                        folium.Marker(location=location, popup=popup).add_to(self.Map)

        if MAP_DRAW_LINE:
            folium.PolyLine(locations=location_list).add_to(self.Map)

        print("Save map data ...")
        self.Map.save(self.FileName)
        print("Map saved in " + self.FileName)
