import gtk
import gconf

from gettext import gettext as _

from gnomeblog import gconf_widgets
from gnomeblog import hig_alert
from gnomeblog import blog

gconf_prefix = None

class LeftLabel(gtk.Label):
    def __init__(self, string):
        gtk.Label.__init__(self, string)
        self.set_alignment(0.0, 0.5)

class BloggerPrefs(gtk.Dialog):
    def __init__(self, prefs_key):
        gtk.Dialog.__init__(self, title=_("Blogger Preferences"), buttons=(gtk.STOCK_CLOSE, gtk.RESPONSE_CLOSE))

        global gconf_prefix
        gconf_prefix = prefs_key

        client = gconf.client_get_default()
        client.add_dir(gconf_prefix, gconf.CLIENT_PRELOAD_ONELEVEL)

        self.set_border_width(5)
        self.set_resizable(False)
        self.set_has_separator(False)

        self.vbox.set_spacing(2)

        blogTypeMenu = gconf_widgets.OptionMenu(gconf_prefix + "/blog_type")
        blogTypeMenu.setStringValuePairs([("blogs.gnome.org", "blogs.gnome.org"),
                                          ("Blogger.com", "blogger.com"),
                                          ("Advogato", "advogato.org"),
                                          ("LiveJournal", "livejournal.com"),
                                          ("-", ""),
                                          (_("Self-Run MovableType"), "custom-mt"),
                                          (_("Self-Run Pyblosxom"), "custom-pybloxsom"),
                                          (_("Self-Run WordPress"), "custom-wordpress"),
                                          (_("Self-Run Other"), "custom")])

        blogTypeBox = gtk.HBox()
        blogTypeBox.set_spacing(12)
        blogTypeBox.pack_start(LeftLabel(_("Blog Type:")), expand=False)
        blogTypeBox.pack_end(blogTypeMenu)



        self.blogProtocolMenu = gconf_widgets.OptionMenu(gconf_prefix + "/blog_protocol")
        self.blogProtocolMenu.setStringValuePairs([("BloggerAPI", "bloggerAPI"),
                                                   ("Advogato", "advogato"),
                                                   ("LiveJournal", "livejournal"),
                                                   ("MetaWeblog", "MetaWeblog")])
        self.blogProtocolLabel = LeftLabel(_("Blog Protocol:"))

        self.urlEntry = gconf_widgets.Entry(gconf_prefix + "/xmlrpc_url")
        self.urlEntry.set_width_chars(45)
        self.urlLabel = LeftLabel(_("Blog Base URL:"))

	self.blogLabel = LeftLabel(_("Blog Name:"))
        self.blogMenu = gconf_widgets.OptionMenu(gconf_prefix + "/blog_id")
        self.lookupButton = gtk.Button(_("Lookup Blogs"))
        self.lookupButton.connect("clicked", self._onLookupBlogsButton)


        table = gtk.Table(rows=4, columns=3)
        table.set_row_spacings(6)
        table.set_col_spacings(12)

        table.attach(self.blogProtocolLabel, 0, 1, 0, 1, xoptions=gtk.FILL)
        table.attach(self.urlLabel, 0, 1, 1, 2, xoptions=gtk.FILL)
        table.attach(LeftLabel(_("Username:")), 0, 1, 2, 3, xoptions=gtk.FILL)
        table.attach(LeftLabel(_("Password:")), 0, 1, 3, 4, xoptions=gtk.FILL)
        table.attach(self.blogLabel, 0, 1, 4, 5, xoptions=gtk.FILL)

        table.attach(self.blogProtocolMenu, 1, 3, 0, 1)
        table.attach(self.urlEntry, 1, 3, 1, 2)
        table.attach(gconf_widgets.Entry(gconf_prefix + "/blog_username"), 1, 3, 2, 3)
        table.attach(gconf_widgets.Entry(gconf_prefix + "/blog_password", True), 1, 3, 3, 4)
        table.attach(self.blogMenu, 1, 2, 4, 5)
        table.attach(self.lookupButton, 2, 3, 4, 5, xoptions=gtk.FILL)

        vbox = gtk.VBox()
        vbox.pack_start(blogTypeBox)
        vbox.pack_start(gtk.HSeparator())
        vbox.pack_start(table)
        vbox.set_spacing(6)
        vbox.set_border_width(5)

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

        lookup = True

	print 'blog type: ' + blog_type

        if blog_type == "custom":
            url = None
            url_ending = ""
            protocol = None
            url_description = _("XML-RPC URL:")
        elif blog_type == "custom-mt":
            url = None
            url_ending = "/mt-xmlrpc.cgi"
            protocol = "MetaWeblog"
            url_description = _("Base Blog URL:")
        elif blog_type == "custom-pybloxsom":
            url = None
            url_ending = "/RPC"
            protocol = "bloggerAPI"
            url_description = _("Base Blog URL:")
        elif blog_type == "custom-wordpress":
            url = None
            url_ending = "/wordpress/xmlrpc.php"
            protocol = "MetaWeblog"
            url_description = _("Base Blog URL:")
        elif blog_type == "blogs.gnome.org":
            url = "http://blogs.gnome.org/xmlrpc/"
            url_ending = ""
            protocol = "MetaWeblog"
            url_description = _("XML-RPC URL:")
        elif blog_type == "blogger.com":
            url = "http://www.blogger.com/api/RPC2"
            url_ending = ""
            protocol = "bloggerAPI"
            url_description = _("XML-RPC URL:")
        elif blog_type == "advogato.org":
            url = "http://www.advogato.org/XMLRPC"
            url_ending = ""
            protocol = "advogato"
            url_description = _("XML-RPC URL:")
	    lookup = False
        elif (blog_type == "livejournal.com"):
            url = "http://www.livejournal.com/interface/xmlrpc"
            url_ending = ""
            protocol = "livejournal"
            url_description = _("XML-RPC URL:")
	    lookup = False
        else:
            url = None
            url_ending = ""
            protocol = None
            url_description = None
            lookup = False
            hig_alert.reportError(_("Unknown blog type"), _("The detected blog type is not among the list of supported blogs"))

        if url != None:
            self.urlEntry.set_sensitive(False)
            self.urlLabel.set_sensitive(False)
            client.set_string(gconf_prefix + "/xmlrpc_url", url)
        else:
            self.urlEntry.set_sensitive(True)
            self.urlLabel.set_sensitive(True)

        if protocol != None:
            self.blogProtocolMenu.set_sensitive(False)
            self.blogProtocolLabel.set_sensitive(False)
            print 'Setting: ' + gconf_prefix + '/blog_protocol' + ' to ' + protocol
            client.set_string(gconf_prefix + "/blog_protocol", protocol)
        else:
            self.blogProtocolMenu.set_sensitive(True)
            self.blogProtocolLabel.set_sensitive(True)

        if url_description:
            self.urlLabel.set_text(url_description)

        client.set_string(gconf_prefix + "/url_ending", url_ending)

	self.lookupButton.set_sensitive(lookup)
        self.blogMenu.set_sensitive(lookup)
        self.blogLabel.set_sensitive(lookup)

    def _onLookupBlogsButton (self, button):
        client = gconf.client_get_default()

        blog_id_pairs = blog.getBlogList(gconf_prefix)

        self.blogMenu.setStringValuePairs(blog_id_pairs)


if __name__ == '__main__':
    dialog = BloggerPrefs ("/apps/gnome-blog")
    dialog.run ()
