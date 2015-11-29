from math import *

class IdConverter(object):
    """description of class"""
    DimX
    DimY
    ColumnMajor

    def __init__(self, dimX, dimY, columnMajor):
        self.DimX = dimX
        self.DimY = dimY
        self.ColumnMajor = columnMajor

    def Convert2dTo1d(self, x, y):
        return y * self.DimX + x if self.ColumnMajor else x * self.DimY + y
    
    def Convert1dTo2d(self, id):
        return (floor(id / self.DimX), id % self.DimX) if self.ColumnMajor else (floor(id / self.DimY), id % self.DimY)

