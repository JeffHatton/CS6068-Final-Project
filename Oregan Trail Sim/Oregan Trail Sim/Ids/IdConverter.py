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
            return int(x * self.DimY + y) if self.ColumnMajor else int(y * self.DimX + x)
    
    def Convert1dTo2d(self, id):
        if id > (self.DimX * self.DimY -1) :
            return (-1,-1)
        else:
            return  (int(floor(id / self.DimY)), int(id % self.DimY)) if self.ColumnMajor else (int(id % self.DimX), int(floor(id / self.DimX)))

