import pygtk
pygtk.require('2.0')

import gtk
import gconf

gconf_prefix = "/apps/gnome-blogger/"

class GConfEntry(gtk.Entry):
    def _onGConfChange (self, client, cnxn_id, entry):
        print ("Changed")
        self.set_text(entry.value.to_string())

    def _onEntryChange (self, entry):
        text = entry.get_text()
        print ("Start")
        self.client.set_string(gconf_key, entry)
        print ("Done")
        
    def __init__(self, gconf_key):
        gtk.Entry.__init__(self)

        self.gconf_key = gconf_key

        self.client = gconf.client_get_default()
        self.client.notify_add (gconf_key, self._onGConfChange)
        
        self.set_text(self.client.get_string(gconf_key))

        self.connect("changed", self._onEntryChange)
        

class LeftLabel(gtk.Label):
    def __init__(self, string):
        gtk.Label.__init__(self, string)
        self.set_alignment(0.0, 0.5)
        
class BloggerPrefs(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self, title="Blogger Preferences", buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))

        self.set_border_width(6)
        self.set_has_separator(gtk.FALSE)

        self.vbox.set_spacing(12)

        table = gtk.Table(rows=4, columns=2)
        table.set_row_spacings(12)
        table.set_col_spacings(6)
        
        table.attach(LeftLabel("BloggerAPI URL:"), 0, 1, 0, 1)
        table.attach(LeftLabel("Username:"), 0, 1, 1, 2)
        table.attach(LeftLabel("Password:"), 0, 1, 2, 3)
        table.attach(LeftLabel("Blog ID:"), 0, 1, 3, 4)

        global gconf_prefix
        
        table.attach(GConfEntry(gconf_prefix + "xmlrpc_url"), 1, 2, 0, 1)
        table.attach(GConfEntry(gconf_prefix + "blog_username"), 1, 2, 1, 2)
        table.attach(GConfEntry(gconf_prefix + "blog_password"), 1, 2, 2, 3)
        table.attach(GConfEntry(gconf_prefix + "blog_id"), 1, 2, 3, 4)

        self.vbox.pack_start(table)

        table.show_all()
        
