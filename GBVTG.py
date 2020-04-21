#!/usr/bin/env python
from VTG import VTG


class GBVTG(VTG):
    def __init__(self):
        VTG.__init__(self)

        self.DataType = "$GBVTG"
