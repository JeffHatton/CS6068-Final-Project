import wpf
#import Actors.Actor
#import Data.DataStore
#import Actors.VilagerActor
#import Tiles.Tile
import time

from threading import Timer
from System.Windows import Application, UserControl


class TileControl(UserControl):
    def __init__(self, tile):
        wpf.LoadComponent(self, 'TileControl.xaml')
        self.Tile = tile
        self.typeLabel = tile.ResourceType

    def refresh(self):
        self.typeLabel = self.Tile.ResourceType
        self.numberLabel = self.Tile.GetActorCount()