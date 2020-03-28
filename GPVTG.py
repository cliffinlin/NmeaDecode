#!/usr/bin/env python
from VTG import VTG


class GPVTG(VTG):
    def __init__(self):
        VTG.__init__(self)

        self.DataType = "$GPVTG"
