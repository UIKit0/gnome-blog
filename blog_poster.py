import pygtk
pygtk.require('2.0')

import gtk
import gconf
import xmlrpclib

gconf_prefix = "/apps/gnome-blogger/"
appkey = "gnome-blogger"

class BlogPoster(gtk.Frame):
    def __init__(self):
        gtk.Frame.__init__(self)
        self.set_shadow_type(gtk.SHADOW_OUT)
        
        box = gtk.VBox()

        self.blogBuffer  = gtk.TextBuffer()
        self.blogEntry   = gtk.TextView(self.blogBuffer)
        scroller         = gtk.ScrolledWindow()
        self.postButton  = gtk.Button("Post Entry")
        
        self.blogEntry.set_editable(gtk.TRUE)

        scroller.add(self.blogEntry)
        scroller.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroller.set_size_request(300, 200)
        scroller.set_shadow_type(gtk.SHADOW_IN)
        
        self.postButton.connect("clicked", self.onPostButtonClicked)
        self.postButtonAlignment = gtk.Alignment(xalign=1.0)
        self.postButtonAlignment.add(self.postButton)
        
        box.pack_start(scroller)
        box.pack_start(self.postButtonAlignment, expand=gtk.FALSE)

        self.add(box)
        box.show_all()

    def onPostButtonClicked(self, button):
        global gconf_prefix, appkey
        
        entryText = self.blogBuffer.get_text(self.blogBuffer.get_start_iter(),
                                             self.blogBuffer.get_end_iter())

        # Don't post silly blog entries like blank ones
        if (not self.postIsReasonable(entryText)):
            return

        client = gconf.client_get_default()
        
        username = client.get_string(gconf_prefix + "blog_username")
        password = client.get_string(gconf_prefix + "blog_password")
        blog_id  = client.get_string(gconf_prefix + "blog_id")
        url      = client.get_string(gconf_prefix + "xml_rpc_url")

        server = xmlrpclib.Server(url)
        #FIXME: handle exceptions
        server.blogger.newPost(appkey, blog_id, username, password,
                               entryText, 1)

        self.blogBuffer.delete(self.blogBuffer.get_start_iter(),
                               self.blogBuffer.get_end_iter())
        
        print ("Posting blog:\n%s" % (entryText))

    def postIsReasonable(self, text):
        # Popup a dialogue confirming even if its deemed
        # unreasonable
        if (text == ""):
            return false
        else:
            return true
