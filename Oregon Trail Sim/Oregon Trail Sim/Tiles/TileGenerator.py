from Tiles import Tile
import random

class TileGenerator(object):
    """description of class"""

    @staticmethod
    def generateTileGrid(dimX, dimY, dataStore, seed=None):
        random.seed(seed)
        listOfTiles = list()
        for x in range(dimX):
            for y in range(dimY):
                randInt = random.randint(0,12)
                tile = Tile.Tile(dataStore)
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
                    tile.Walkable = False
                elif randInt == 4:
                    tile.ResourceType = "Iron"                    

                listOfTiles.append(tile)
                random.seed(None)
        return listOfTiles
