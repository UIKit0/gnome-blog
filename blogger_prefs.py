import gtk
import gconf

from gnomeblog import gconf_widgets
from gnomeblog import hig_alert
from gnomeblog import blog

gconf_prefix = "/apps/gnome-blogger"

class LeftLabel(gtk.Label):
    def __init__(self, string):
        gtk.Label.__init__(self, string)
        self.set_alignment(0.0, 0.5)
        
class BloggerPrefs(gtk.Dialog):
    def __init__(self, prefs_key):
        gtk.Dialog.__init__(self, title="Blogger Preferences", buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))

        global gconf_prefix

        if (prefs_key != None):
            gconf_prefix = prefs_key

        client = gconf.client_get_default()
        client.add_dir(gconf_prefix, gconf.CLIENT_PRELOAD_ONELEVEL)

        self.set_border_width(6)
        self.set_has_separator(gtk.FALSE)

        self.vbox.set_spacing(12)

        blogTypeMenu = gconf_widgets.OptionMenu(gconf_prefix + "/blog_type")
        blogTypeMenu.setStringValuePairs([("Blogger.com", "blogger.com"),
                                         ("Advogato", "advogato.org"),
                                         ("-", ""),
                                         ("Self-Run MovableType", "custom-mt"),
                                         ("Self-Run Pybloxsom", "custom-pybloxsom"),
                                         ("Self-Run Other", "custom")])

        blogTypeBox = gtk.HBox()
        blogTypeBox.set_spacing(6)
        blogTypeBox.pack_start(LeftLabel("Blog Type:"), expand=gtk.FALSE)
        blogTypeBox.pack_end(blogTypeMenu)



        self.blogProtocolMenu = gconf_widgets.OptionMenu(gconf_prefix + "/blog_protocol")
        self.blogProtocolMenu.setStringValuePairs([("BloggerAPI", "bloggerAPI"),
                                                   ("Advogato", "advogato"),
                                                   ("MetaWeblog", "MetaWeblog")])
        self.blogProtocolLabel = LeftLabel("Blog Protocol:")
        
        self.urlEntry = gconf_widgets.Entry(gconf_prefix + "/xmlrpc_url")
        self.urlEntry.set_width_chars(45)
        self.urlLabel = LeftLabel("Blog Base URL:")

	self.blogLabel = LeftLabel("Blog Name:")
        self.blogMenu = gconf_widgets.OptionMenu(gconf_prefix + "/blog_id")
        self.lookupButton = gtk.Button("Lookup Blogs")
        self.lookupButton.connect("clicked", self._onLookupBlogsButton)


        table = gtk.Table(rows=4, columns=3)
        table.set_row_spacings(12)
        table.set_col_spacings(6)

        table.attach(self.blogProtocolLabel, 0, 1, 0, 1, xoptions=gtk.FILL)
        table.attach(self.urlLabel, 0, 1, 1, 2, xoptions=gtk.FILL)
        table.attach(LeftLabel("Username:"), 0, 1, 2, 3, xoptions=gtk.FILL)
        table.attach(LeftLabel("Password:"), 0, 1, 3, 4, xoptions=gtk.FILL)
        table.attach(self.blogLabel, 0, 1, 4, 5, xoptions=gtk.FILL)

        table.attach(self.blogProtocolMenu, 1, 3, 0, 1)
        table.attach(self.urlEntry, 1, 3, 1, 2)
        table.attach(gconf_widgets.Entry(gconf_prefix + "/blog_username"), 1, 3, 2, 3)
        table.attach(gconf_widgets.Entry(gconf_prefix + "/blog_password", gtk.TRUE), 1, 3, 3, 4)
        table.attach(self.blogMenu, 1, 2, 4, 5)
        table.attach(self.lookupButton, 2, 3, 4, 5, xoptions=gtk.FILL)

        vbox = gtk.VBox()
        vbox.pack_start(blogTypeBox)
        vbox.pack_start(gtk.HSeparator())
        vbox.pack_start(table)
        vbox.set_spacing(12)
        vbox.set_border_width(6)
        
        self.vbox.pack_start(vbox)

        vbox.show_all()

        self.notify = client.notify_add(gconf_prefix + "/blog_type", self._gconfBlogTypeChange)
        blog_type = client.get_string(gconf_prefix + "/blog_type")
        self._updateBlogType(blog_type)
        

    def _gconfBlogTypeChange (self, client, cnxn_id, entry, what):
        blog_type = entry.value.get_string()

        self._updateBlogType(blog_type)

    def _updateBlogType(self, blog_type):
        client = gconf.client_get_default()

        lookup = gtk.TRUE

	print 'blog type: ' + blog_type

        if (blog_type == "custom"):
            url = None
            protocol = None
            url_description = "XML-RPC URL:"
        elif (blog_type == "custom-mt"):
            url = None
            protocol = "MetaWeblog"
            url_description = "Base Blog URL:"
        elif (blog_type == "custom-pybloxsom"):
            url = None
            protocol = "bloggerAPI"
            url_description = "Base Blog URL:"
        elif (blog_type == "blogger.com"):
            url = "http://plant.blogger.com/api/RPC2"
            protocol = "bloggerAPI"
            url_description = "XML-RPC URL:"
        elif (blog_type == "advogato.org"):
            url = "http://www.advogato.org/XMLRPC"
            protocol = "advogato"
            url_description = "XML-RPC URL:"
	    lookup = gtk.FALSE
        else:
            # FIXME: popup an error dialog
            print ("Unknown blog type (!)")

        if (url != None):
            self.urlEntry.set_sensitive(gtk.FALSE)
            self.urlLabel.set_sensitive(gtk.FALSE)
            client.set_string(gconf_prefix + "/xmlrpc_url", url)
        else:
            self.urlEntry.set_sensitive(gtk.TRUE)
            self.urlLabel.set_sensitive(gtk.TRUE)

        if (protocol != None):
            self.blogProtocolMenu.set_sensitive(gtk.FALSE)
            self.blogProtocolLabel.set_sensitive(gtk.FALSE)
            print 'Setting: ' + gconf_prefix + '/blog_protocol' + ' to ' + protocol
            client.set_string(gconf_prefix + "/blog_protocol", protocol)
        else:
            self.blogProtocolMenu.set_sensitive(gtk.TRUE)
            self.blogProtocolLabel.set_sensitive(gtk.TRUE)

        if (url_description):
            self.urlLabel.set_text(url_description)

	self.lookupButton.set_sensitive(lookup)
        self.blogMenu.set_sensitive(lookup)
        self.blogLabel.set_sensitive(lookup)

    def _onLookupBlogsButton (self, button):
        client = gconf.client_get_default()

        blog_id_pairs = blog.getBlogList(gconf_prefix)

        self.blogMenu.setStringValuePairs(blog_id_pairs)
    
