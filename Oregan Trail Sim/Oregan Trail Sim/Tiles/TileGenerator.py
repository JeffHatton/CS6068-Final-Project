from Tiles import Tile
import random

class TileGenerator(object):
    """description of class"""

    @staticmethod
    def generateTileGrid(dimX, dimY):
        listOfTiles = list()
        for x in range(dimX):
            for y in range(dimY):
                randInt = random.randint(0,10)
                tile = Tile.Tile()
                tile.ID.IdX = x
                tile.ID.IdY = y
               
                if randInt == 0:
                    tile.ResourceType = "Wood"
                elif randInt == 1:
                    tile.ResourceType = "Food"
                elif randInt == 2:
                    tile.ResourceType = "Stone"
                elif randInt == 3:
                    tile.ResourceType = "Water"
                    #tile.Walkable = False

                listOfTiles.append(tile)
        return listOfTiles
