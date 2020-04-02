#!/usr/bin/env python

import gmplot

import Coordtransform
from BaseMap import BaseMap

MAP_DRAW_LINE = True

MAP_DRAW_MARK = True
MAP_DRAW_MARK_COLOR_PDOP = True
MAP_DRAW_MARK_COLOR_FIX_QUALITY = True

MAP_DRAW_MARK_DURATION_IN_SECOND = 10


class GMPlotMap(BaseMap):
    def __init__(self):
        BaseMap.__init__(self)
        self.Map = gmplot.GoogleMapPlotter(
            center_lat=self.CenterLocation[0],
            center_lng=self.CenterLocation[1],
            zoom=self.Zoom
        )

    def draw(self):
        print("\n")
        print("Prepare data to draw...")
        if self.NavigateDataList is None or len(self.NavigateDataList) == 0:
            print("No data to draw!")
            return

        # location_list = []
        latitude_list = []
        longitude_list = []

        for navigate_data in self.NavigateDataList:
            if navigate_data is None:
                continue

            if navigate_data.LatitudeValue is None or navigate_data.LongitudeValue is None:
                continue

            # print("navigate_data=" + navigate_data.to_string())

            # location = [navigate_data.LatitudeValue, navigate_data.LongitudeValue]
            # location_list.append(location)
            gcj_lng, gcj_lat = Coordtransform.wgs84_to_gcj02(navigate_data.LongitudeValue, navigate_data.LatitudeValue)
            # latitude_list.append(navigate_data.LatitudeValue)
            # longitude_list.append(navigate_data.LongitudeValue)
            latitude_list.append(gcj_lat)
            longitude_list.append(gcj_lng)

            # if MAP_DRAW_MARK:
            #     if self.check_mark_duration(navigate_data):
            #         popup = navigate_data.to_string()
            #
            #         self.set_mark_color(navigate_data)
            #
            #         if self.MarkColor is not None:
            #             folium.Marker(location=location, popup=popup, icon=folium.Icon(color=self.MarkColor)).add_to(
            #                 self.Map)
            #         else:
            #             folium.Marker(location=location, popup=popup).add_to(self.Map)

        if MAP_DRAW_LINE:
            # folium.PolyLine(locations=location_list).add_to(self.Map)
            self.Map.plot(latitude_list, longitude_list,
                          'cornflowerblue', edge_width=2.5)

        print("Save map data ...")
        self.Map.draw(self.FileName)
        print("Map saved in " + self.FileName)
