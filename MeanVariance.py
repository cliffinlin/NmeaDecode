#!/usr/bin/env python
import numpy

SEPARATE_STRING = ",\t"


class MeanVariance:
    def __init__(self):
        self.DataType = ""
        self.Separate = SEPARATE_STRING

        self.DataList = None

        self.Mean = None
        self.Var = None
        self.Std = None

    def set_data_list(self, data_type, data_list):
        self.DataType = data_type
        if len(data_list) == 0:
            return

        self.DataList = numpy.array(data_list).astype(numpy.float)

    def mean(self):
        if self.DataList is None:
            return

        self.Mean = numpy.mean(self.DataList)

    def var(self):
        if self.DataList is None:
            return

        self.Var = numpy.var(self.DataList)

    def std(self):
        if self.DataList is None:
            return

        self.Std = numpy.std(self.DataList)

    def statistic(self, data_type, data_list):
        self.set_data_list(data_type, data_list)

        self.mean()
        self.var()
        self.std()

        print(self.to_string())

    def mean_to_string(self):
        result = ""

        if self.Mean is None:
            return result

        result += "Mean="
        result += str(self.Mean)
        result += self.Separate

        return result

    def var_to_string(self):
        result = ""

        if self.Var is None:
            return result

        result += "Var="
        result += str(self.Var)
        result += self.Separate

        return result

    def std_to_string(self):
        result = ""

        if self.Std is None:
            return result

        result += "Std="
        result += str(self.Std)
        result += self.Separate

        return result

    def to_string(self):
        result = ""

        result += self.DataType + self.Separate

        result += self.mean_to_string() \
                  + self.var_to_string() \
                  + self.std_to_string()

        return result
