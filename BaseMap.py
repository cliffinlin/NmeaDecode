#!/usr/bin/env python

FILE_NAME_EXT_HTML = '.html'

MAP_DEFAULT_CENTER_LOCATION = [39.9032, 116.3915]
MAP_DEFAULT_ZOOM = 12


class BaseMap:
    def __init__(self):
        self.CenterLocation = MAP_DEFAULT_CENTER_LOCATION
        self.Zoom = MAP_DEFAULT_ZOOM

        self.FileName = None

    def set_file_name(self, file_name):
        self.FileName = file_name + FILE_NAME_EXT_HTML