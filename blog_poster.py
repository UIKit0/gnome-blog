import pygtk
pygtk.require('2.0')

import gtk
import pango
import gconf

import xmlrpclib

import hig_alert
import style_toggle

gconf_prefix = "/apps/gnome-blogger"
appkey = "6BF507937414229AEB450AB075001667C8BC8338"

class BlogPoster(gtk.Frame):
    def __init__(self, prefs_key):
        gtk.Frame.__init__(self)
        self.set_shadow_type(gtk.SHADOW_OUT)

        if (prefs_key != None):
            global gconf_prefix
            gconf_prefix = prefs_key
        
        box = gtk.VBox()
        box.set_border_width(6)
        box.set_spacing(6)
        
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
        
        self.postButton.connect("clicked", self._onPostButtonClicked)
        self.postButtonAlignment = gtk.Alignment(xalign=1.0, yalign=0.5)
        self.postButtonAlignment.add(self.postButton)

        buttonBox = gtk.HBox()
        buttonBox.set_spacing(6)
        buttonBox.pack_end(self.postButtonAlignment)

        bold_tag = self.blogBuffer.create_tag("bold", weight=pango.WEIGHT_BOLD)
        boldToggle = style_toggle.StyleToggle(gtk.STOCK_BOLD, bold_tag, "strong", self.blogEntry)
        
        italic_tag = self.blogBuffer.create_tag("italic", style=pango.STYLE_ITALIC)
        italic_tag.html_tag = "em"
        italicToggle = style_toggle.StyleToggle(gtk.STOCK_ITALIC, italic_tag, "em", self.blogEntry)
        
        buttonBox.pack_start(boldToggle, expand=gtk.FALSE)
        buttonBox.pack_start(italicToggle, expand=gtk.FALSE)        

        box.pack_start(scroller)
        box.pack_start(buttonBox)

        self.add(box)
        box.show_all()

 
    def _postEntry (self, username, password, blog_id, url, text):
        if (url == None):
            hig_alert.reportError("Could not post Blog entry", "No XML-RPC server URL to post blog entries to is set, or the value could not be retrieved from GConf. Your entry will remain in the blogger window.")
            return gtk.FALSE

        success = gtk.TRUE

        print ("Getting server...")

        server = xmlrpclib.Server(url)

        try:
            print ("Doing post")
            server.blogger.newPost(appkey, blog_id, username, password,
                                   text, xmlrpclib.True)
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, "Could not post blog entry", username, blog_id, url)
            success = gtk.FALSE
        except xmlrpclib.ProtocolError, e:
            hig_alert.reportError("Could not post Blog entry", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: <span style=\"italic\">%s</span>.' % (url, e.errmsg))
            success = gtk.FALSE

        print ("Success is....")
        print (success)

        return success

    def _getHTMLText(self, buffer):
        html = ""
        
        iter = buffer.get_start_iter()
        tagFound = gtk.TRUE

        open_tags = []
        
        while(tagFound == gtk.TRUE):
            turnontags = iter.get_toggled_tags(gtk.TRUE)
            turnofftags = iter.get_toggled_tags(gtk.FALSE)

            for tag in turnofftags:
                tags_to_reopen = []
                opentag = open_tags.pop()
                while (opentag != tag):
                    html = html + opentag.closing_tag
                    tags_to_reopen.append(opentag)
                    opentag = open_tags.pop()

                html = html + tag.closing_tag

                for reopen in tags_to_reopen:
                    open_tags.append(reopen)
                    html = html + reopen.opening_tag
            
            for tag in turnontags:
                open_tags.append(tag)
                html = html + tag.opening_tag

                
                
            last_iter = iter.copy()
            tagFound = iter.forward_to_tag_toggle(None)
            if (not tagFound):
                iter = buffer.get_end_iter()

            new_text = buffer.get_text(last_iter, iter)
            html = html + new_text

        return html
        
    def _onPostButtonClicked(self, button):
        global gconf_prefix, appkey
        
        html_text = self._getHTMLText(self.blogBuffer)

        # Don't post silly blog entries like blank ones
        if (not self.postIsReasonable(html_text)):
            return

        client = gconf.client_get_default()
        
        username = client.get_string(gconf_prefix + "blog_username")
        password = client.get_string(gconf_prefix + "blog_password")
        blog_id  = client.get_string(gconf_prefix + "blog_id")
        url      = client.get_string(gconf_prefix + "xmlrpc_url")

        print ("Text %s" % html_text)

        successful_post = self._postEntry(username, password, blog_id, url, html_text)

        if (successful_post):
            # Only delete the entry if posting was successful
            self.blogBuffer.delete(self.blogBuffer.get_start_iter(),
                                   self.blogBuffer.get_end_iter())

    def postIsReasonable(self, text):
        # Popup a dialogue confirming even if its deemed
        # unreasonable
        if (text == None or text == ""):
            hig_alert.reportError("Blog Entry is Blank", "No text was entered in the blog entry box. Please enter some text and try again")
            return gtk.FALSE
        else:
            return gtk.TRUE
