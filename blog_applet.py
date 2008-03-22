#!/usr/bin/env python
import pygtk
pygtk.require('2.0')

import gtk
import gobject
import gnome
import gnomeapplet
import gconf
import string  # maybe someone can do this trick without string?

from gettext import gettext as _, bindtextdomain, textdomain

from gnomeblog import blog_poster
from gnomeblog import aligned_window
from gnomeblog import blogger_prefs
from gnomeblog import gnome_blog_globals

bindtextdomain('gnome-blog', gnome_blog_globals.localedir)
textdomain('gnome-blog')

gtk.window_set_default_icon_name('gnome-blog')
        
class BloggerApplet(gnomeapplet.Applet):
    def __init__(self):
        self.__gobject_init__()

    def init(self):
        self.set_applet_flags(gnomeapplet.EXPAND_MINOR)
        self.toggle = gtk.ToggleButton()
	self.toggle.set_relief(gtk.RELIEF_NONE)
        self.applet_tooltips = gtk.Tooltips()
        self.setup_menu_from_file (None, "GNOME_BlogApplet.xml",
                                   None, [(_("About"), self._showAboutDialog), ("Pref", self._openPrefs)])

        button_box = gtk.HBox()
        button_box.pack_start(gtk.Label(_("Blog")))
        self.arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_IN)
        button_box.pack_start(self.arrow)

        self.toggle.add(button_box)
        
        self.add(self.toggle)
        self.toggle.connect("toggled", self._onToggle)
        self.toggle.connect("button-press-event", self._onButtonPress)
        
	self.set_background_widget(self)
        self.show_all()

        self.poster_window = aligned_window.AlignedWindow(self.toggle, self.get_orient)
        accel_group = gtk.AccelGroup()
        self.poster_window.add_accel_group(accel_group)
        self.prefs_key = self.get_preferences_key()
        print "Applet prefs located at %s" % (self.prefs_key)
        self.poster = blog_poster.BlogPosterSimple(prefs_key=self.prefs_key,
                                                   on_entry_posted=self._onEntryPosted,
                                                   accel_group=accel_group)
        self.poster_window.add(self.poster)
        self.poster.show()

        client = gconf.client_get_default()
        value = client.get_bool(self.prefs_key + "/initialized")
        if value == None or value == False:
            self.poster._showPrefDialog()
#            self._showPrefDialog()
            client.set_bool(self.prefs_key + "/initialized", True)

        self._createToolTip(client)
        
        return True
    
    def _showAboutDialog(self, uicomponent, verb):
        about = gtk.AboutDialog()
        about.set_name(gnome_blog_globals.name)
        about.set_version(gnome_blog_globals.version)
        about.set_copyright("Copyright 2003 Seth Nickell")
        about.set_comments(_("A GNOME Web Blogging Applet"))
        about.set_authors(["Seth Nickell <seth@gnome.org>"])
        about.set_translator_credits(_("translator-credits"))
        about.set_logo_icon_name('gnome-blog')
        about.connect("response", lambda dialog, response: dialog.destroy())
        about.show()

    def _showPrefDialog(self):
        prefs_dialog = blogger_prefs.BloggerPrefs(self.prefs_key)
        prefs_dialog.show()
        prefs_dialog.run()
        prefs_dialog.hide()
        
    def _openPrefs(self, uicomponent, verb):
        self._showPrefDialog()
        
    def _onToggle(self, toggle):
        if toggle.get_active():
            self.poster_window.positionWindow()            
            self.poster_window.show()
            self.poster.grab_focus()
        else:
            self.poster_window.hide()

    def _onEntryPosted(self):
        self.toggle.set_active(False)

    def _onButtonPress(self, toggle, event):
        if event.button != 1:
            toggle.stop_emission("button-press-event")
            
    def _createToolTip(self,client):
        # take the XML_RPC value from GConf
        blog_url = client.get_string(self.prefs_key + "/xmlrpc_url")
        # split the URL up into http:, '', domainname, extra
        blog_split = string.split(blog_url,"/",3);
        # join back up the URL into http://domainname
        blog_url = string.join(blog_split[:3],"/")

        tooltip = _("Create a blog entry for %s at %s") % \
                  ( client.get_string(self.prefs_key + "/blog_username"), \
                    blog_url )
        
        # Set tooltip to the applet button
        self.applet_tooltips.set_tip(self.toggle,tooltip)        

        

gobject.type_register(BloggerApplet)


def foo(applet, iid):
    print "Returning blogger applet"
    return applet.init()

gnomeapplet.bonobo_factory("OAFIID:GNOME_BlogApplet_Factory", 
                            BloggerApplet.__gtype__, 
                            "Blog", "0", foo)

print "Done waiting in factory, returning... If this seems wrong, perhaps there is another copy of the Blog factory running?"
