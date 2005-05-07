import gtk

from gettext import gettext as _

def italic(s):
	return "<span style=\"italic\">%s</span>" % s

def bold(s):
	return "<span weight=\"bold\">%s</span>" % s

def handleBloggerAPIFault(e, primary, username, blog_id, url):
    if e.faultCode == 'Method Error':
        reportError(primary, _('URL \'%s\' may not be a valid bloggerAPI. XML-RPC Server reported: %s.') % (url, italic(e.faultString)))
    elif e.faultCode == 'PasswordError':
        reportError(primary, _('Unknown username %s or password trying to post blog entry to XML-RPC server %s.') % (bold(username), italic(url)))
    elif e.faultCode == 'PostError':
        reportError(primary, _('Could not post to blog \'%s\' at bloggerAPI XML-RPC server \'%s\'. Server reported: %s.') % (blog_id, url, italic(e.faultString)))
    else:
        reportError(primary, _('The bloggerAPI server (%s) reported an error I don\'t understand: \'%s, %s\'. \n\nPlease email this error message to seth@gnome.org so I can address it.') % (url, italic(e.faultCode), e.faultString))

def reportError(primaryText, secondaryText):
    alert = HIGAlert(primaryText, secondaryText,
                     buttons = (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    alert.run()
    alert.hide()

class HIGAlert(gtk.Dialog):
    def __init__(self, primaryText, secondaryText, parent=None, flags=0, buttons=None):
        gtk.Dialog.__init__(self, primaryText, parent, flags, buttons)

        self.set_border_width(6)
        self.set_has_separator(False)
        self.set_resizable(False)

        self.vbox.set_spacing(12)

        hbox = gtk.HBox()
        hbox.set_spacing(12)
        hbox.set_border_width(6)
        
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG)
        alignment = gtk.Alignment(yalign=0.0)
        alignment.add(image)
        hbox.pack_start(alignment, expand=False)

        
        vbox = gtk.VBox()

        primaryLabel = gtk.Label("")
        primaryLabel.set_use_markup(True)
        primaryLabel.set_markup('<span weight="bold" size="larger">%s</span>\n' % (primaryText))
        primaryLabel.set_line_wrap(True)
        primaryLabel.set_alignment(0.0, 0.0)
        primaryLabel.set_selectable(True)
        
        secondaryLabel = gtk.Label("")
        secondaryLabel.set_use_markup(True)
        secondaryLabel.set_markup(secondaryText)
        secondaryLabel.set_line_wrap(True)
        secondaryLabel.set_alignment(0.0, 0.0)
        secondaryLabel.set_selectable(True)
        
        vbox.pack_start(primaryLabel)
        vbox.pack_end(secondaryLabel)
        hbox.pack_end(vbox)

        hbox.show_all()

        self.vbox.add(hbox)
        
