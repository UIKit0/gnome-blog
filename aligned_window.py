import pygtk
pygtk.require('2.0')

import gtk

class AlignedWindow(gtk.Window):

    def __init__(self, widgetToAlignWith):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_decorated(gtk.FALSE)
        
        self.widgetToAlignWith = widgetToAlignWith

    def positionWindow(self):
        # Get our own dimensions & position
        self.show()
        self.realize()
        ourWidth  = (self.window.get_geometry())[2]
        ourHeight = (self.window.get_geometry())[3]

        # Get the dimensions/position of the widgetToAlignWith
        self.widgetToAlignWith.realize()
        (entryX, entryY) = self.widgetToAlignWith.window.get_origin()
        entryWidth  = (self.widgetToAlignWith.window.get_geometry())[2]
        entryHeight = (self.widgetToAlignWith.window.get_geometry())[3]

        # Get the screen dimensions
        screenHeight = gtk.gdk.screen_height()
        screenWidth = gtk.gdk.screen_width()

        if entryX + ourWidth < screenWidth:
            # Align to the left of the entry
            newX = entryX
        else:
            # Align to the right of the entry
            newX = (entryX + entryWidth) - ourWidth

        if entryY + entryHeight + ourHeight < screenHeight:
            # Align to the bottom of the entry
            newY = entryY + entryHeight
        else:
            newY = entryY - ourHeight

        # -"Coordinates locked in captain."
        # -"Engage."
        self.move(newX, newY)

