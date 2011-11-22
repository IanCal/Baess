import kivy
kivy.require('1.0.9') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.uix.filechooser import FileChooserIconView


classesToColours = {
   'knot' : (1,1,0,0.5), 
   'bridge' : (0,0,1,0.5), 
   'other' : (1,0,0,0.5), 
   'sectioning_artifact' : (0,1,1,0.5), 
   'cant_tell' : (0.5,0.7,0.8,0.5),
   'unclassified' : (0.1,0.1,0.1,0.5)
}


class MyPaintWidget(Widget):
    def drawSelf(self):
        with self.canvas:
            d = 30.
            Ellipse(pos=(self.x, self.y), size=(d, d))
    def setClass(self, classification):
        self.colour = classesToColours[classification]
    def setInactive(self):
        self.canvas.clear()
        with self.canvas:
            Color(self.colour[0], self.colour[1], self.colour[2], self.colour[3])
        self.drawSelf()
    def setActive(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 0, 1, 0.5)
        self.drawSelf()

class Point():
    def __init__(self, pos):
        self.scatter = Scatter(size_hint=(0.05,0.05))
        self.widget = MyPaintWidget()
        self.widget.setClass('unclassified')
        self.widget.setActive()
        self.scatter.x = pos[0]
        self.scatter.y = pos[1]
        self.scatter.add_widget(self.widget)

    def setOnPress(self, callback):
        self.scatter.bind(on_touch_down=callback)
        
    def setInactive(self):
        self.widget.setInactive()
    def setActive(self):
        self.widget.setActive()

    def setClassification(self, classification):
        self.classification = classification
        self.widget.setClass(classification)

    def setPos(self, pos):
        self.scatter.x = pos[0]
        self.scatter.y = pos[1]

    def getDisplay(self):
        return self.scatter

    def getPos(self):
        return (self.scatter.x, self.scatter.y)


class Track():
    def __init__(self, activecallback):
        self.points = {}
        self.active = False
        self.setOnActive(activecallback)
    def addPoint(self, point, layer):
        if (len(self.points) > 0):
            if (self.points.has_key(layer)):
                return False
            if not(self.points.has_key(layer - 1) or self.points.has_key(layer + 1)):
                return False
        if (self.points.has_key(layer - 1)):
            point.setPos(self.points[layer - 1].getPos())
        if (self.points.has_key(layer + 1)):
            point.setPos(self.points[layer + 1].getPos())
        if (self.active):
            point.setActive()
        else:
            point.setInactive()
        point.setOnPress(self.onActiveCallback)
        self.points[layer] = point
        return True
    def getClassification(self):
        return self.classification

    def setClassification(self, classification):
        self.classification = classification
        for point in self.points.values():
            point.setClassification(classification)

    def setOnActive(self, callback):
        def wrapped(ev,touch):
            callback(self)
        self.onActiveCallback = wrapped
        
    def getPointForLayer(self, layer):
        if (self.points.has_key[layer]):
            return self.points[layer]
        return None
    def setActive(self):
        self.active = True
        for point in self.points.values():
            point.setActive()
    def setInactive(self):
        self.active = False
        for point in self.points.values():
            point.setInactive()

class Layer():
    def __init__(self, img):
        self.points = []
        self.layout = FloatLayout(size=(600, 600))
        self.layout.add_widget(Image(source=img))
    def addPoint(self, point):
        self.points.append(point)
        self.layout.add_widget(point.getDisplay())
    def getContents(self):
        return self.layout

layers = []
for img in [ 
        "images/L1CnorS1a3.tif.png", \
        "images/L1CnorS2a3.tif.png", \
        "images/L1CnorS3a3.tif.png", \
        "images/L1CnorS4a3.tif.png", \
        "images/L1CnorS5a3.tif.png", \
        "images/L1CnorS6a3.tif.png", \
        "images/L1CnorS7a3.tif.png", \
        "images/L1CnorS8a3.tif.png", \
        "images/L1CnorS9a3.tif.png", \
        "images/L1CnorS10a3.tif.png"]:
    layers.append(Layer(img))


class Menu:
    def __init__(self):
        self.layout = GridLayout(cols=1)#anchor_x='right', anchor_y='top')
        button =Button(text='New Track')
        button.bind(on_press=self.addTrack)
        self.layout.add_widget(button)
        button2 =Button(text='New Point On Track')
        button2.bind(on_press=self.addPoint)
        self.layout.add_widget(button2)
        for classification in classesToColours.keys():
            button = Button(text=classification)
            button.bind(on_press=self.setClass(classification))
            self.layout.add_widget(button)
        self.showStatsButton = Button(text='Print Statistics')
        self.layout.add_widget(self.showStatsButton)

    def onShowStats(self, callback):
        self.showStatsButton.bind(on_press=callback)

    def setClass(self, classification):
        def wrapped(*args):
            self.onSetClassCallback(classification)
        return wrapped

    def onSetClass(self, callback):
        self.onSetClassCallback = callback

    def onNewPoint(self, callback):
        self.newPointCallback = callback
        
    def addPoint(self, more):
        self.newPointCallback()

    def onNewTrack(self, callback):
        self.newTrackCallback = callback
        
    def addTrack(self, more):
        self.newTrackCallback()

    def getContents(self):
        return self.layout


class MyApp(App):
    def build(self):
        Window.bind(on_key_down=self.on_key_down) 
        self.tracks = []
        self.activeTrack = None
        self.currentLayer = 0
        self.appstructure = GridLayout(cols=2)
        self.menu = Menu()
        self.menu.onNewTrack(self.newTrack)
        self.menu.onNewPoint(self.newPoint)
        self.menu.onSetClass(self.setClass)
        self.menu.onShowStats(self.showStats)
        self.core = Widget()
        self.core.add_widget(self.getCurrentLayer().getContents())
        self.appstructure.add_widget(self.core)
        self.appstructure.add_widget(self.menu.getContents())
        return self.appstructure

    def showStats(self, *args):
        classCounts = {}
        for classification in classesToColours:
            classCounts[classification] = 0
        for track in self.tracks:
            classCounts[track.getClassification()] += 1
        print "Statistics:"
        for classification in classCounts:
            print "    ", classification, " : ", classCounts[classification]

    def setClass(self, classification):
        if (self.activeTrack):
            self.activeTrack.setClassification(classification)

    def setActive(self, track):
        if (self.activeTrack):
            self.activeTrack.setInactive()
        self.activeTrack = track
        track.setActive()
    def newPoint(self):
        point = Point((200,200))
        if (self.activeTrack.addPoint(point, self.currentLayer)):
            self.getCurrentLayer().addPoint(point)
        

    def newTrack(self):
        track = Track(self.setActive)
        point = Point((200,200))
        track.addPoint(point, self.currentLayer)
        track.setActive()
        track.setClassification('unclassified')
        self.tracks.append(track)
        self.setActive(track)
        self.getCurrentLayer().addPoint(point)
    def getCurrentLayer(self):
        return layers[self.currentLayer]

    def moveUpLayer(self):
        if (self.currentLayer < (len(layers) - 1)):
            original = self.getCurrentLayer()
            self.currentLayer += 1
            new = self.getCurrentLayer()
            self.swapLayer(original, new)
    def moveDownLayer(self):
        if (self.currentLayer > 0):
            original = self.getCurrentLayer()
            self.currentLayer -= 1
            new = self.getCurrentLayer()
            self.swapLayer(original, new)

    def swapLayer(self, layer1, layer2):
        self.core.add_widget(layer2.getContents())
        self.core.remove_widget(layer1.getContents())
    def on_key_down(self, instance, code, *args):
        if (code == 275):
            self.moveUpLayer()
        if (code == 276):
            self.moveDownLayer()

if __name__ in ('__android__', '__main__'):
    MyApp().run()

