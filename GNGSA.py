#!/usr/bin/env python
from GSA import GSA

GNGSA_INDEX_SYSTEM_ID = 17

GNGSA_DATA_LENGTH_MIN = GNGSA_INDEX_SYSTEM_ID + 1


class GNGSA(GSA):
    def __init__(self):
        GSA.__init__(self)

        self.DataType = "$GNGSA"

        self.SystemId = ""

    def decode(self, line):
        result = True

        GSA.decode(self, line)

        if self.Data is None:
            return result

        if len(self.Data) < GNGSA_DATA_LENGTH_MIN:
            return result

        self.SystemId = self.Data[GNGSA_INDEX_SYSTEM_ID]

        print(self.to_string())

        result = True

        return result

    def system_id_to_string(self):
        result = ""

        if self.SystemId is None or len(self.SystemId) == 0:
            return result

        result += "SystemId="

        value = int(self.SystemId)
        if value == 1:
            result += "GPS"
        elif value == 2:
            result += "GLO"
        elif value == 4:
            result += "BDS"

        return result

    def to_string(self):
        result = ""

        if len(self.Sentence) == 0:
            return result

        result = GSA.to_string(self)

        result += self.system_id_to_string()

        return result
