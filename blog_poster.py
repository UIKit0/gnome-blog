import gtk
import pango
import gconf

from gettext import gettext as _

from gnomeblog import hig_alert
from gnomeblog import rich_entry
from gnomeblog import blog
from gnomeblog import blogger_prefs

#check if pygtkspell is installed
try:
    import gtkspell
    use_gtkspell = 1
except:
    use_gtkspell = 0

gconf_prefix = None

class BlogPoster(gtk.Frame):
    def __init__(self, prefs_key="/apps/gnome-blog", on_entry_posted=None, accel_group=None):
        gtk.Frame.__init__(self)
        self.set_shadow_type(gtk.SHADOW_OUT)

        self.on_entry_posted = on_entry_posted

        global gconf_prefix
        gconf_prefix = prefs_key

        print "Using gconf_prefix %s" % (gconf_prefix)
            
        box = gtk.VBox()
        box.set_border_width(6)
        box.set_spacing(6)
        
        self.blogEntry   = rich_entry.RichEntry()

	#if we are using gtkspell, attach it to the blogEntry
	if use_gtkspell:
		gtkspell.Spell(self.blogEntry)

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
        
        if (accel_group):
            boldToggle.add_accelerator("clicked", accel_group, ord("B"),
                                       gtk.gdk.CONTROL_MASK, 0)
            italicToggle.add_accelerator("clicked", accel_group, ord("I"),
                                         gtk.gdk.CONTROL_MASK, 0)

        self.prefs_button = gtk.Button(_("Preferences..."))
        self.prefs_button.connect("clicked", self._onPrefsButtonClicked)

        buttonBox.pack_start(boldToggle, expand=False)
        buttonBox.pack_start(italicToggle, expand=False)        
        buttonBox.pack_start(linkButton, expand=False)
        buttonBox.pack_start(self.prefs_button, expand=False)
            
        self.titleEntry = gtk.Entry()

        titleBox = gtk.HBox()
        titleBox.set_spacing(12)
        titleBox.pack_start(gtk.Label(_("Title:")), expand=False)
        titleBox.pack_start(self.titleEntry)

        box.pack_start(titleBox, expand=False)
        box.pack_start(scroller)
        box.pack_start(buttonBox, expand=False)

        self.add(box)
        box.show_all()

        self.titleEntry.connect('activate', lambda entry,box=box: box.child_focus(gtk.DIR_TAB_FORWARD))

        self.titleEntry.connect('changed', self._checkEmptyPost)
        self.blogEntry.buffer.connect('changed', self._checkEmptyPost)
        self._checkEmptyPost()

    def _checkEmptyPost(self, *args):
        sensitive = 1
        if not self.titleEntry.get_text().strip():
            sensitive = 0
        start,end = self.blogEntry.buffer.get_bounds()
        if not start.get_visible_slice(end).strip():
            sensitive = 0
        self.postButton.set_sensitive(sensitive)
        
    def _onPostButtonClicked(self, button):
        global gconf_prefix, appkey

        images = self.blogEntry.getImages()

        try:
            for image in images:
                image.uri = blog.uploadImage(image, gconf_prefix)
                image.opening_tag = '<img src="%s"/>' % (image.uri)
        except blog.FeatureNotSupported, e:
            hig_alert.reportError(_("Couldn't upload images"), _("The blog protocol in use does not support uploading images"))

        #we must turn off the spell checker so as not to confuse
        #the markup to html converter
        if use_gtkspell:
            spell = gtkspell.get_from_text_view(self.blogEntry)
            spell.detach()
        
        html_text = self.blogEntry.getHTML()

	#turn spelling back on
        if use_gtkspell:
            gtkspell.Spell(self.blogEntry)

        print "Text is: {\n %s \n }\n" % (html_text)
        title = self.titleEntry.get_text().decode('utf-8')

        # Don't post silly blog entries like blank ones
        if not self._postIsReasonable(html_text):
            return

        successful_post = blog.postEntry(title, html_text, gconf_prefix)

        if successful_post:
            # Only delete the entry if posting was successful
            self._clearBlogEntryText()
            # Call back our parent informing them the entry was posted
            if self.on_entry_posted != None:
                self.on_entry_posted()

    def _clearBlogEntryText(self):
        self.blogEntry.clear()
        self.titleEntry.delete_text(0, -1)

    def _onPrefsButtonClicked(self, button):
        self._showPrefDialog()

    def _showPrefDialog(self):
        prefs_dialog = blogger_prefs.BloggerPrefs(gconf_prefix)
        prefs_dialog.show()
        prefs_dialog.run()
        prefs_dialog.hide()

    def _postIsReasonable(self, text):
        # Popup a dialogue confirming even if its deemed
        # unreasonable
        if not text:
            hig_alert.reportError(_("Blog Entry is Blank"), _("No text was entered in the blog entry box. Please enter some text and try again"))
            return False
        else:
            return True

class BlogPosterSimple(BlogPoster):
    def __init__(self, prefs_key="/apps/gnome-blog", on_entry_posted=None, accel_group=None):
        BlogPoster.__init__(self, prefs_key, on_entry_posted, accel_group)
        self.prefs_button.hide_all();
