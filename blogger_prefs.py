import pygtk
pygtk.require('2.0')

import gtk
import gconf

import xmlrpclib

import gconf_widgets
import hig_alert

gconf_prefix = "/apps/gnome-blogger"

class LeftLabel(gtk.Label):
    def __init__(self, string):
        gtk.Label.__init__(self, string)
        self.set_alignment(0.0, 0.5)
        
class BloggerPrefs(gtk.Dialog):
    def __init__(self):
        gtk.Dialog.__init__(self, title="Blogger Preferences", buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))

        global gconf_prefix
        
        client = gconf.client_get_default()
        client.add_dir(gconf_prefix, gconf.CLIENT_PRELOAD_ONELEVEL)

        self.set_border_width(6)
        self.set_has_separator(gtk.FALSE)

        self.vbox.set_spacing(12)

##        blogTypeOptionMenu = gtk.OptionMenu()
##        blogTypeOptionMenu.url_list = []

##        blogTypeMenu = gtk.Menu()
##        blogTypeMenu.append(gtk.MenuItem("Self-Hosted Blog"))
##        blogTypeOptionMenu.url_list.append("")
##        blogTypeMenu.append(gtk.MenuItem("Blogger.com"))
##        blogTypeOptionMenu.url_list.append("http://plant.blogger.com/api/RPC2")
##        blogTypeMenu.show_all()
        
##        menu = blogTypeOptionMenu.set_menu(blogTypeMenu)

##        blogTypeOptionMenu.connect("changed", self._onBlogTypeChanged)
##        blogTypeOptionMenu.set_history(0)

        blogTypeBox = gtk.HBox()
        blogTypeBox.pack_start(gconf_widgets.CheckButton("Blog is on blogger.com",
                                                         gconf_prefix + "/use_blogger_dot_com"))
##        blogTypeBox.pack_start(LeftLabel("Blog Type:"))
##        blogTypeBox.pack_end(blogTypeOptionMenu)

        table = gtk.Table(rows=4, columns=3)
        table.set_row_spacings(12)
        table.set_col_spacings(6)
        
        table.attach(LeftLabel("BloggerAPI URL:"), 0, 1, 0, 1, xoptions=gtk.FILL)
        table.attach(LeftLabel("Username:"), 0, 1, 1, 2, xoptions=gtk.FILL)
        table.attach(LeftLabel("Password:"), 0, 1, 2, 3, xoptions=gtk.FILL)
        table.attach(LeftLabel("Blog Name:"), 0, 1, 3, 4, xoptions=gtk.FILL)

        self.urlEntry = gconf_widgets.Entry(gconf_prefix + "/xmlrpc_url")
        self.urlEntry.set_width_chars(45)
        table.attach(self.urlEntry, 1, 3, 0, 1)
        table.attach(gconf_widgets.Entry(gconf_prefix + "/blog_username"), 1, 3, 1, 2)
        table.attach(gconf_widgets.Entry(gconf_prefix + "/blog_password"), 1, 3, 2, 3)
##        table.attach(gconf_widgets.Entry(gconf_prefix + "/blog_id"), 1, 2, 3, 4)

        self.blogMenu = gconf_widgets.OptionMenu(gconf_prefix + "/blog_id")
        table.attach(self.blogMenu, 1, 2, 3, 4)

        lookupButton = gtk.Button("Lookup Blogs")
        lookupButton.connect("clicked", self._onLookupBlogsButton)

        table.attach(lookupButton, 2, 3, 3, 4)

        self.notify = client.notify_add(gconf_prefix + "/use_blogger_dot_com", self._gconfUseBloggerChange)

        vbox = gtk.VBox()
        vbox.pack_start(blogTypeBox)
        vbox.pack_start(gtk.HSeparator())
        vbox.pack_start(table)
        vbox.set_spacing(12)
        
        self.vbox.pack_start(vbox)

        vbox.show_all()

    def _gconfUseBloggerChange (self, client, cnxn_id, entry, what):
        use_blogger = entry.value.get_bool()
        if (use_blogger):
            self.urlEntry.set_sensitive(gtk.FALSE)
            client.set_string(gconf_prefix + "/xmlrpc_url", "http://plant.blogger.com/api/RPC2")
        else:
            self.urlEntry.set_sensitive(gtk.TRUE)
            
##    def _onBlogTypeChanged(self, optionmenu):
##        index = optionmenu.get_history()
##        url = optionmenu.url_list[index]

##        print ("URL is %s" % url)
        
##        client = gconf.client_get_default()
##        client.set_string(gconf_prefix + "/xmlrpc_url", url)

    def _onLookupBlogsButton (self, button):
        client = gconf.client_get_default()
                
        username = client.get_string(gconf_prefix + "/blog_username")
        password = client.get_string(gconf_prefix + "/blog_password")
        url      = client.get_string(gconf_prefix + "/xmlrpc_url")

        appkey = "6BF507937414229AEB450AB075001667C8BC8338"
        
        server = xmlrpclib.Server(url)

        try:
            bloglist = server.blogger.getUsersBlogs(appkey, username, password)
        except xmlrpclib.Fault, e:
            hig_alert.reportError("Could not get list of Blogs", "bloggerAPI server reported: '%s'" % (e))
            return

        if ((bloglist == None) or (len(bloglist) == 0)):
            # No blogs found!
            hig_alert.reportError("No Blogs Found", "No errors were reported, but no blogs were found at %s for username %s\n" % ( url, username))
            return

        string_value_pairs = []

        for blog in bloglist:
            string_value_pairs.append((blog["blogName"], blog["blogid"]))

        self.blogMenu.setStringValuePairs(string_value_pairs)
        
