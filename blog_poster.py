import gtk
import pango
import gconf

import gettext
_ = gettext.gettext

from gnomeblog import hig_alert
from gnomeblog import rich_entry
from gnomeblog import blog

gconf_prefix = "/apps/gnome-blogger"

class BlogPoster(gtk.Frame):
    def __init__(self, prefs_key):
        gtk.Frame.__init__(self)
        self.set_shadow_type(gtk.SHADOW_OUT)

        global gconf_prefix

        if (prefs_key != None):
            gconf_prefix = prefs_key

        print ("Using gconf_prefix %s" % (gconf_prefix))
            
        box = gtk.VBox()
        box.set_border_width(6)
        box.set_spacing(6)
        
        self.blogEntry   = rich_entry.RichEntry()
        scroller         = gtk.ScrolledWindow()
        self.postButton  = gtk.Button(_("_Post Entry"))
        
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

        boldToggle   = self.blogEntry.createStyleToggle([("weight", pango.WEIGHT_BOLD)], gtk.STOCK_BOLD, "strong")
        italicToggle = self.blogEntry.createStyleToggle([("style", pango.STYLE_ITALIC)], gtk.STOCK_ITALIC, "em")        
        linkButton   = rich_entry.InsertHyperlinkButton(self.blogEntry)
        
        #link_tag = self.blogBuffer.create_tag("a")
        #link_tag.set_property("underline", pango.UNDERLINE_SINGLE)
        #link_tag.set_property("foreground", "#0000FF")
        #linkButton = InsertButton

        buttonBox.pack_start(boldToggle, expand=gtk.FALSE)
        buttonBox.pack_start(italicToggle, expand=gtk.FALSE)        
        buttonBox.pack_start(linkButton, expand=gtk.FALSE)
        
        self.titleEntry = gtk.Entry()

        titleBox = gtk.HBox()
        titleBox.set_spacing(6)
        titleBox.pack_start(gtk.Label(_("Title:")), expand=gtk.FALSE)
        titleBox.pack_start(self.titleEntry)

        box.pack_start(titleBox)
        box.pack_start(scroller)
        box.pack_start(buttonBox)

        self.add(box)
        box.show_all()


        
    def _onPostButtonClicked(self, button):
        global gconf_prefix, appkey
        
        html_text = self.blogEntry.getHTML()
        print ("Text is: {\n %s \n }\n" % (html_text))
        title = self.titleEntry.get_text()

        # Don't post silly blog entries like blank ones
        if (not self._postIsReasonable(html_text)):
            return

        successful_post = blog.postEntry(title, html_text, gconf_prefix)

        if (successful_post):
            # Only delete the entry if posting was successful
            self._clearBlogEntryText()

    def _clearBlogEntryText(self):
        self.blogEntry.clear()
        self.titleEntry.delete_text(0, -1)
        

    def _postIsReasonable(self, text):
        # Popup a dialogue confirming even if its deemed
        # unreasonable
        if (text == None or text == ""):
            hig_alert.reportError(_("Blog Entry is Blank", "No text was entered in the blog entry box. Please enter some text and try again"))
            return gtk.FALSE
        else:
            return gtk.TRUE
