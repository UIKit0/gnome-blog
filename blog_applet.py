#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import gtk
import gobject
import gnome.applet

import blog_poster
import aligned_window
import blogger_prefs
import gconf

class BloggerApplet(gnome.applet.Applet):
    def __init__(self):
        self.__gobject_init__()

    def init(self):
        self.toggle = gtk.ToggleButton()
        verbs = ("Pref", self._openPrefs)

        self.setup_menu_from_file (None, "GNOME_BlogApplet.xml",
                                   None, [("Pref", self._openPrefs)])

        button_box = gtk.HBox()
        button_box.pack_start(gtk.Label("Blog"))
        self.arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_IN)
        button_box.pack_start(self.arrow)

        self.toggle.add(button_box)
        
        self.add(self.toggle)
        self.toggle.connect("toggled", self._onToggle)
        self.toggle.connect("button-press-event", self._onButtonPress)
        self.show_all()

        self.poster_window = aligned_window.AlignedWindow(self.toggle)
        self.poster_window.set_modal(gtk.TRUE)
        self.prefs_key = self.get_preferences_key()
        print ("Applet prefs located at %s" % (self.prefs_key))
        self.poster = blog_poster.BlogPoster(self.prefs_key)
        self.poster_window.add(self.poster)
        self.poster.show()

        client = gconf.client_get_default()
        value = client.get_bool(self.prefs_key + "/initialized")
        if (value == None or value == gtk.FALSE):
            self._showPrefDialog()
            client.set_bool(self.prefs_key + "/initialized", gtk.TRUE)
        
        return gtk.TRUE
    
    def _showPrefDialog(self):
        prefs_dialog = blogger_prefs.BloggerPrefs(self.prefs_key)
        prefs_dialog.show()
        prefs_dialog.run()
        prefs_dialog.hide()
        
    def _openPrefs(self, uicomponent, verb):
        self._showPrefDialog()
        
    def _onToggle(self, toggle):
        if (toggle.get_active()):
            self.poster_window.positionWindow()            
            self.poster_window.show()
            self.poster.grab_focus()
        else:
            self.poster_window.hide()

    def _onButtonPress(self, toggle, event):
        if (event.button != 1):
            toggle.stop_emission("button-press-event")
            
        

gobject.type_register(BloggerApplet)


def foo(applet, iid):
    print ("Returning blogger applet")
    return applet.init()

gnome.applet.bonobo_factory("OAFIID:GNOME_BlogApplet_Factory", 
                            BloggerApplet.__gtype__, 
                            "Blog", "0", foo)

print ("Done waiting in factory, returning... If this seems wrong, perhaps there is another copy of the Blog factory running?")
