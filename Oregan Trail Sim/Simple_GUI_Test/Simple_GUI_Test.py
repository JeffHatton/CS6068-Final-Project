import wpf
import Actors.Actor
import Data.DataStore
import Actors.VilagerActor
import Tiles.Tile
import time

from threading import Timer
from System.Windows import Application, Window

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'Simple_GUI_Test.xaml')


        #for x in range(10):
        #    for y in range(10):
        #dataStore = Data.DataStore.DataStore(10,10)

        #for x in range(10):
        #    for y in range(10):
        #        tile = Tiles.Tile.Tile()
        #        tile.ID.IdX = x
        #        tile.ID.IdY = y
        #        tile.ID.LocalId = dataStore.TileIdConverter.Convert2dTo1d(x,y)

        #        tileControl = TileControl(tile)
        #        Grid.SetRow(box, x);
        #        Grid.SetColumn(box, y);

        #        self.grid.Children.Add(box);

        #        dataStore.AddTile(tile)

        #for x in range(5):
        #    actor = Actors.VilagerActor.VilagerActor(dataStore, dataStore.EnvTiles[5])
        #    dataStore.AddActor(actor)

        #for key, value in dataStore.EnvTiles.iteritems():
        #    print("{0}: {1}").format(key, value.GetActorCount())
        #print("")
        #print("")
        #print("")


        #for key, value in dataStore.EnvActors.iteritems():
        #    value.start()

        #while True:
        #    for key, value in dataStore.EnvTiles.iteritems():
        #        print("{0}: {1}").format(key, value.GetActorCount())
        #    print("")
        #    print("")
        #    print("")
        #    time.sleep(1)
    
    def refresh(self):
        t = Timer(1, refresh)
        t.start()

if __name__ == '__main__':
    Application().Run(MyWindow())
    



