#!/usr/bin/python
import gtk
import gnomeapplet

class AlignedWindow(gtk.Window):

    def __init__(self, widgetToAlignWith, orient_func):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_decorated(False)
        
        self.widgetToAlignWith = widgetToAlignWith
        self.get_orient = orient_func

    def positionWindow(self):
        # Get our own dimensions & position
        self.realize()
        gtk.gdk.flush()
        ourWidth  = (self.window.get_geometry())[2]
        ourHeight = (self.window.get_geometry())[3]

        # Skip the taskbar, and the pager, stick and stay on top
        self.stick()
        self.set_keep_above(True)
        self.set_skip_pager_hint(True)
        self.set_skip_taskbar_hint(True)
        self.set_type_hint (gtk.gdk.WINDOW_TYPE_HINT_DOCK)

        # Get the dimensions/position of the widgetToAlignWith
        self.widgetToAlignWith.realize()
        (x, y) = self.widgetToAlignWith.window.get_origin()

        (w, h) = self.get_size()
        (w, h) = self.size_request()

        button_w = self.widgetToAlignWith.allocation.width
        button_h = self.widgetToAlignWith.allocation.height

        screen = self.get_screen()

        found_monitor = False
        n = screen.get_n_monitors()
        for i in range(0, n):
                monitor = screen.get_monitor_geometry(x)
                if (x >= monitor.x and x <= monitor.x + monitor.width and \
                    y >= monitor.y and y <= monitor.y + monitor.height):
                        found_monitor = True
                        break
        
        if not found_monitor:
                monitor = gtk.gdk.Rectangle(0, 0, screen.get_width(), screen.get_width())
        
        orient = self.get_orient()
        if orient == gnomeapplet.ORIENT_RIGHT:
                x += button_w

                if ((y + ourHeight) > monitor.y + monitor.height):
                        y -= (y + h) - (monitor.y + monitor.height)
                
                if ((y + h) > (monitor.height / 2)):
                        gravity = gtk.gdk.GRAVITY_SOUTH_WEST
                else:
                        gravity = gtk.gdk.GRAVITY_NORTH_WEST
        elif orient == gnomeapplet.ORIENT_LEFT:
                x -= w

                if ((y + h) > monitor.y + monitor.height):
                        y -= (y + h) - (monitor.y + monitor.height)
                
                if ((y + h) > (monitor.height / 2)):
                        gravity = gtk.gdk.GRAVITY_SOUTH_EAST
                else:
                        gravity = gtk.gdk.GRAVITY_NORTH_EAST
        elif orient == gnomeapplet.ORIENT_DOWN:
                y += button_h

                if ((x + w) > monitor.x + monitor.width):
                        x -= (x + w) - (monitor.x + monitor.width)

                gravity = gtk.gdk.GRAVITY_NORTH_WEST
        elif orient == gnomeapplet.ORIENT_UP:
                y -= h

                if ((x + w) > monitor.x + monitor.width):
                        x -= (x + w) - (monitor.x + monitor.width)

                gravity = gtk.gdk.GRAVITY_SOUTH_WEST
        
        # -"Coordinates locked in captain."
        # -"Engage."
        self.move(x, y)
        self.set_gravity(gravity)
        self.show()

