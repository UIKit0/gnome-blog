import pygtk
pygtk.require('2.0')

import gtk

def handleBloggerAPIFault(e, primary, username, blog_id, url):
    if (e == 'Method Error'):
        reportError(primary, 'URL \'%s\' may not be a valid bloggerAPI. XML-RPC Server reported: <span style=\"italic\">%s</span>.' % (url, e.faultString))
    elif (e == 'PasswordError'):
        reportError(primary, 'Invalid username (%s) or password trying to post blog entry to XML-RPC server \'%s\'.' % (username, url))
    elif (e == 'PostError'):
        reportError(primary, 'Could not post to blog \'%s\' at bloggerAPI XML-RPC server \'%s\'. Server reported: <span style=\"italic\">%s</span>.' % (blog_id, url, e.faultString))
    else:
        reportError(primary, 'The bloggerAPI server (%s) reported an error I don\'t understand: \'%s\'. \n\nPlease email this error message to seth@gnome.org so I can address it.' % (url, e.faultString))

def reportError(primaryText, secondaryText):
    alert = HIGAlert(primaryText, secondaryText,
                     buttons = (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    alert.run()
    alert.hide()

class HIGAlert(gtk.Dialog):
    def __init__(self, primaryText, secondaryText, parent=None, flags=0, buttons=None):
        gtk.Dialog.__init__(self, primaryText, parent, flags, buttons)

        self.set_border_width(6)
        self.set_has_separator(gtk.FALSE)
        self.set_resizable(gtk.FALSE)

        self.vbox.set_spacing(12)

        hbox = gtk.HBox()
        hbox.set_spacing(12)
        hbox.set_border_width(6)
        
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_DIALOG_ERROR, gtk.ICON_SIZE_DIALOG)
        alignment = gtk.Alignment(yalign=0.0)
        alignment.add(image)
        hbox.pack_start(alignment, expand=gtk.FALSE)

        
        vbox = gtk.VBox()

        primaryLabel = gtk.Label()
        primaryLabel.set_use_markup(gtk.TRUE)
        primaryLabel.set_markup('<span weight="bold" size="larger">%s</span>\n' % (primaryText))
        primaryLabel.set_line_wrap(gtk.TRUE)
        primaryLabel.set_alignment(0.0, 0.0)
        primaryLabel.set_selectable(gtk.TRUE)
        
        secondaryLabel = gtk.Label()
        secondaryLabel.set_use_markup(gtk.TRUE)
        secondaryLabel.set_markup(secondaryText)
        secondaryLabel.set_line_wrap(gtk.TRUE)
        secondaryLabel.set_alignment(0.0, 0.0)
        secondaryLabel.set_selectable(gtk.TRUE)
        
        vbox.pack_start(primaryLabel)
        vbox.pack_end(secondaryLabel)
        hbox.pack_end(vbox)

        hbox.show_all()

        self.vbox.add(hbox)
        
