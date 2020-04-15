#!/usr/bin/env python
import branca
import folium

import Transform
from BaseMap import BaseMap

GOOGLE_MAP = True

DOP_THRESH_HOLD = 5.0

MAP_DRAW_MARK = True
MAP_DRAW_MARK_COLOR_PDOP = True
MAP_DRAW_MARK_COLOR_FIX_QUALITY = True

MAP_DRAW_MARK_DURATION_IN_SECOND = 10


class FoliumMap(BaseMap):
    def __init__(self):
        BaseMap.__init__(self)

        self.Map = None
        self.ColorMap = None
        self.MarkColor = None

        self.LastDateTime = None

        self.LocationList = []

        self.setup_map()

    def setup_map(self):
        if GOOGLE_MAP:
            tiles = 'https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}'  # google 卫星图
        else:
            tiles = 'http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}'  # 高德卫星图

        self.Map = folium.Map(
            location=self.CenterLocation,
            zoom_start=self.Zoom,
            tiles=tiles,
            # tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}', # 高德街道图
            # tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', # 高德卫星图
            # tiles='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', # google 卫星图
            # tiles='https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}', # google 地图
            attr='default'
        )

        self.ColorMap = branca.colormap.StepColormap(
            [(55, 168, 218), (187, 249, 112), (255, 255, 0), (113, 130, 36), (113, 174, 38), (255, 255, 255)],
            vmin=1, vmax=7,
            index=[1, 2, 3, 4, 5, 6, 7],
            caption='Fix Quality: 1=SPS, 2=Differential, 3=PPS, 4=RTK Fixed, 5=RTK Float, 6=Estimated'
        )

        self.Map.add_child(self.ColorMap)
        self.Map.add_child(folium.LatLngPopup())

    def need_map_draw_marker(self, navigate_data):
        result = False

        if not MAP_DRAW_MARK:
            return result

        if navigate_data is None:
            return result

        navigate_data.setup_local_date_time()
        if navigate_data.LocalDateTime is None:
            return result

        if self.LastDateTime is not None:
            duration = navigate_data.LocalDateTime - self.LastDateTime
            if duration.seconds < MAP_DRAW_MARK_DURATION_IN_SECOND:
                return result

        result = True
        self.LastDateTime = navigate_data.LocalDateTime

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
                self.MarkColor = "lightgreen"  # remark = "Differential"
            elif value == 3:
                self.MarkColor = "yellow"  # remark = "PPS"
            elif value == 4:
                self.MarkColor = "darkgreen"  # remark = "RTK Fixed"
            elif value == 5:
                self.MarkColor = "green"  # remark = "RTK Float"
            elif value == 6:
                self.MarkColor = "white"  # remark = "Estimated"

        if MAP_DRAW_MARK_COLOR_PDOP:
            if navigate_data.PDOP is None or len(navigate_data.PDOP) == 0:
                return

            if float(navigate_data.PDOP) > DOP_THRESH_HOLD:
                self.MarkColor = "red"

    def add_navigate_data_list(self, navigate_data_list, color=None):
        print("\n")
        print("Add data to map...")
        if navigate_data_list is None or len(navigate_data_list) == 0:
            print("No data to draw!")
            return

        self.LocationList = []
        for navigate_data in navigate_data_list:
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

            self.LocationList.append(location)

            if self.need_map_draw_marker(navigate_data):
                popup = navigate_data.to_string()

                self.set_mark_color(navigate_data)

                if self.MarkColor is not None:
                    folium.Marker(location=location, popup=popup, icon=folium.Icon(color=self.MarkColor)).add_to(
                        self.Map)
                else:
                    folium.Marker(location=location, popup=popup).add_to(self.Map)

        if color is not None:
            folium.PolyLine(locations=self.LocationList, color=color).add_to(self.Map)
        else:
            folium.PolyLine(locations=self.LocationList).add_to(self.Map)

    def save(self):
        print("Save map data ...")
        self.Map.save(self.FileName)
        print("Map saved in " + self.FileName)
