import pygtk
pygtk.require('2.0')

import gtk
import gconf
import xmlrpclib

import hig_alert

gconf_prefix = "/apps/gnome-blogger/"
appkey = "6BF507937414229AEB450AB075001667C8BC8338"

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
        self.blogEntry.set_wrap_mode(gtk.WRAP_WORD)

        scroller.add(self.blogEntry)
        scroller.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        scroller.set_size_request(400, 300)
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
        url      = client.get_string(gconf_prefix + "xmlrpc_url")

        if (url == None):
            self.reportError("Could not post Blog entry", "No XML-RPC server URL to post blog entries to is set, or the value could not be retrieved from GConf. Your entry will remain in the blogger window.")
            return
        
        server = xmlrpclib.Server(url)

        try:
            server.blogger.newPost(appkey, blog_id, username, password,
                                   entryText, 1)
        except xmlrpclib.Fault, e:
            primary = "Could not post Blog entry"
            if (e == 'Method Error'):
                self.reportError(primary, 'URL \'%s\' may not be a valid bloggerAPI. XML-RPC Server reported: <span style=\"italic\">%s</span>. Your entry will remain in the blogger window.' % (url, e.faultString))
            elif (e == 'PasswordError'):
                self.reportError(primary, 'Invalid username (%s) or password trying to post blog entry to XML-RPC server \'%s\'. Your entry will remain in the blogger window.' % (username, url))
            elif (e == 'PostError'):
                self.reportError(primary, 'Could not post to blog \'%s\' at bloggerAPI XML-RPC server \'%s\'. Server reported: <span style=\"italic\">%s</span>. Your entry will remain in the blogger window.' % (blog_id, url, e.faultString))
        except xmlrpclib.ProtocolError, e:
            self.reportError("Could not post Blog entry", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: <span style=\"italic\">%s</span>. Your entry will remain in the blogger window.' % (url, e.errmsg))
        else:
            # Only delete the entry if posting was successful
            self.blogBuffer.delete(self.blogBuffer.get_start_iter(),
                                   self.blogBuffer.get_end_iter())

            
        
        print ("Posting blog:\n%s" % (entryText))

    def reportError(self, primaryText, secondaryText):
        alert = hig_alert.HIGAlert(primaryText, secondaryText,
                                   buttons = (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        alert.run()
        alert.hide()

    def postIsReasonable(self, text):
        # Popup a dialogue confirming even if its deemed
        # unreasonable
        if (text == None or text == ""):
            return gtk.FALSE
        else:
            return gtk.TRUE
