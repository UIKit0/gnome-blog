import pygtk
pygtk.require('2.0')

import gtk
import gconf

class OptionMenu(gtk.OptionMenu):
    def __init__(self, gconf_key):
        gtk.OptionMenu.__init__(self)

        self.gconf_key = gconf_key

        self.client = gconf.client_get_default()
        self.notify = self.client.notify_add(self.gconf_key, self._onGConfChange)
        
        self.connect("changed", self._onChanged)

    def setStringValuePairs (self, string_value_pairs):
        self.menu = gtk.Menu()
        self.set_menu(self.menu)

        self.values = []

        for string_value_pair in string_value_pairs:
            string = string_value_pair[0]
            value  = string_value_pair[1]
            
            self.menu.append(gtk.MenuItem(string))
            self.values.append(value)
            
        self.menu.show_all()
        gconf_value = self.client.get_string(self.gconf_key)
        self._setMenuFromValue(gconf_value)
        
    def _setMenuFromValue (self, gconf_value):
        i = 0
        for value in self.values:
            print ("Comparing %s and %s" % (value, gconf_value))
            if (value == gconf_value):
                print ("match")
                self.set_history(i)
                break
            i = i + 1
            
    def _onGConfChange (self, client, cnxn_id, entry, what):
        gconf_value = entry.value.to_string()
        self._setMenuFromValue(gconf_value)

    def _onChanged(self, optionmenu):
        index = optionmenu.get_history()
        value = self.values[index]
        
        client = gconf.client_get_default()
        client.set_string(self.gconf_key, value)

class Entry(gtk.Entry):
    def _onGConfChange (self, client, cnxn_id, entry, what):
        self.set_text(entry.value.to_string())

    def _onEntryChange (self, entry):
        text = entry.get_text()
        self.client.set_string(self.gconf_key, text)
        
    def __init__(self, gconf_key):
        gtk.Entry.__init__(self)

        self.gconf_key = gconf_key

        self.client = gconf.client_get_default()
        self.notify = self.client.notify_add(self.gconf_key, self._onGConfChange)
        
        self.set_text(self.client.get_string(self.gconf_key))

        self.connect("changed", self._onEntryChange)

class CheckButton(gtk.CheckButton):
    def _onGConfChange (self, client, cnxn_id, entry, what):
        self.set_active(entry.value.get_bool())

    def _onCheckboxToggled (self, checkbox):
        toggled = checkbox.get_active()
        self.client.set_bool(self.gconf_key, toggled)

    def __init__(self, label, gconf_key):
        gtk.CheckButton.__init__(self, label)

        self.gconf_key = gconf_key

        self.client = gconf.client_get_default()
        self.notify = self.client.notify_add(self.gconf_key, self._onGConfChange)

        self.set_active(self.client.get_bool(self.gconf_key))
        self.connect("toggled", self._onCheckboxToggled)
