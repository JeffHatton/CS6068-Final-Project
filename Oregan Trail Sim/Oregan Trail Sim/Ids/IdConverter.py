from math import *

class IdConverter(object):
    """description of class"""

    def __init__(self, dimX, dimY, columnMajor):
        self.DimX = dimX
        self.DimY = dimY
        self.ColumnMajor = columnMajor

    def Convert2dTo1d(self, x, y):
        if x >= self.DimX or y >= self.DimY or y < 0 or x < 0:
            return -1
        else:
            return x * self.DimY + y if self.ColumnMajor else y * self.DimX + x
    
    def Convert1dTo2d(self, id):
        if id > self.DimX * self.DimY -1 :
            return (-1,-1)
        else:
            return  (floor(id / self.DimY), id % self.DimY) if self.ColumnMajor else (id % self.DimX, floor(id / self.DimX))

