import gtk
import gtk.gdk
import pango
import gobject
import gnome
import gnome.vfs

import gettext
_ = gettext.gettext

from gnomeblog import html_converter
from gnomeblog import hig_alert

class RichEntry(gtk.TextView):
    def __init__(self):
        self.buffer = gtk.TextBuffer()
        gtk.TextView.__init__(self, self.buffer)

        self._initDND()
        
        self.set_editable(gtk.TRUE)
        self.set_wrap_mode(gtk.WRAP_WORD)
        self.set_pixels_below_lines(16)
        
        html_converter.para_tag = self.buffer.create_tag("p")
        html_converter.para_tag.opening_tag = "<p>"
        html_converter.para_tag.closing_tag = "</p>"

        self.connect("event-after", self._onEventAfter)

        # Hack for addHyperlink with old pygtk's
        self.linknum = 0

        self.images = [ ]

    def _initDND(self):
        
        # GtkTextView already defines drag and drop targets, get them
        old_targets = self.drag_dest_get_target_list()

        # Unfortunately old_targets string field has a funny type
        # that needs to be explicitly converted to string
        targets = []
        for target in old_targets:
            targets.append((str(target[0]), target[1], target[2]))

        # Add the DND type that we support and set the new list of types
        targets.append(("text/uri-list", 0, 398))
        self.drag_dest_set_target_list(targets)
        
        self.connect("drag-data-received", self._onDragDataReceived)
        

    def _getUniqueTag(self):
        if (gtk.pygtk_version[0] < 2 and gtk.pygtk_version[1] < 100
            and gtk.pygtk_version[2] < 16):
            # this is an older version of pygtk that doesn't
            # have a way to create anonymous tags, hack around it
            link_tag = self.buffer.create_tag("unique%d" % (self.linknum))
            self.linknum = self.linknum + 1
            print "Old Pygtk, using hack to work around lack of anonymous tags"
        else:
            link_tag = self.buffer.create_tag()
        return link_tag
    
    def addHyperlink(self, iter, text, uri, on_activate):
        link_tag = self._getUniqueTag()
            
        link_tag.set_property("underline", pango.UNDERLINE_SINGLE)
        link_tag.set_property("foreground", "#0000FF")

        link_tag.opening_tag = '<a href="%s">' % (uri)
        link_tag.closing_tag = '</a>'
        
        link_tag.uri = uri
        link_tag.on_activate = on_activate
        link_tag.hyperlink = gtk.TRUE

        self.buffer.insert_with_tags(iter, text, link_tag)

    def applyHyperlink(self, selection, uri, on_activate):
        link_tag = self._getUniqueTag()
            
        link_tag.set_property("underline", pango.UNDERLINE_SINGLE)
        link_tag.set_property("foreground", "#0000FF")

        link_tag.opening_tag = '<a href="%s">' % (uri)
        link_tag.closing_tag = '</a>'
        
        link_tag.uri = uri
        link_tag.on_activate = on_activate
        link_tag.hyperlink = gtk.TRUE

        self.buffer.apply_tag(link_tag, selection[0], selection[1])

    def getImages(self):
        return self.images
        
    def getHTML(self):
        return html_converter.getHTML(self.buffer)

    def clear(self):
        self.buffer.delete(self.buffer.get_start_iter(),
                           self.buffer.get_end_iter())

    def createStyleToggle(self, pango_markup_properties, stock_button, html_tag):
        tag = self.buffer.create_tag(html_tag)
        for property in pango_markup_properties:
            tag.set_property(property[0], property[1])
        return StyleToggle(stock_button, tag, html_tag, self)

    def _onDragDataReceived(self, widget, drag_context, window_x, window_y,
                            selection_data, info, timestamp):
        if (info == 398):
            # 398 means text/uri-list
            assert(selection_data.format == 8)
            uri_list = selection_data.data
            uris = uri_list.split('\r\n')

            (buffer_x, buffer_y) = self.window_to_buffer_coords(gtk.TEXT_WINDOW_WIDGET,
                                                                window_x, window_y)

            dnd_iter = self.get_iter_at_location(buffer_x, buffer_y)
            
            for uri in uris:
                if (len(uri) <= 0):
                    continue

                loader = gtk.gdk.PixbufLoader()

                try:
                    file_info = gnome.vfs.get_file_info(uri, gnome.vfs.FILE_INFO_GET_MIME_TYPE)
                    file_contents = gnome.vfs.read_entire_file(uri)
                except gnome.vfs.Error, e:
                    i_uri = "<span style='italic'>" + uri + "</span>"
                    hig_alert.reportError(_("Could not load dragged in image"),
                                          _("Error loading %s was: %s") % (i_uri, e))
                loader.write(file_contents)
                try:
                    loader.close()
                    pixbuf = loader.get_pixbuf()                    
                except gobject.GError, e:
                    pixbuf = None
                    i_uri = "<span style='italic'>" + uri + "</span>"
                    hig_alert.reportError(_("Could not load dragged in image"),
                                          _("Error loading %s was: %s") % (i_uri, e))
                    
                if (pixbuf):
                    # Create a new image tag
                    image_tag = self._getUniqueTag()
                    image_tag.opening_tag = ""
                    image_tag.closing_tag = ""
                    image_tag.file_contents = file_contents
                    paths = uri.split('/')
                    image_tag.name = paths[len(paths) - 1]
                    image_tag.mime_type = file_info.mime_type

                    self.images.append(image_tag)
                    
                    # Insert the pixbuf, and then set the new image
                    # tag around it so that we can generate its HTML later
                    start_offset = dnd_iter.get_offset()

                    self.buffer.insert_pixbuf(dnd_iter, pixbuf)
                    
                    start = self.buffer.get_iter_at_offset(start_offset)
                    self.buffer.apply_tag(image_tag, start, dnd_iter)
            
        else:
            print ("Some other sort of data received")
        
    def _onEventAfter(self, widget, event):
        if event.type != gtk.gdk.BUTTON_RELEASE or event.button != 1:
            return gtk.FALSE

        bounds = self.buffer.get_selection_bounds()
        if not bounds:
            return gtk.FALSE

        x, y = self.window_to_buffer_coords (gtk.TEXT_WINDOW_WIDGET, int(event.x), int(event.y))

        iter = self.get_iter_at_location(x, y)

        for tag in iter.get_tags():
            try:
                if tag.hyperlink == gtk.TRUE:
                    # Found Hyperlink, activating
                    tag.on_activate(tag.uri)
            except AttributeError:
                pass
            
        return gtk.FALSE

class InsertHyperlinkButton(gtk.Button):
    def __init__(self, rich_entry):
        gtk.Button.__init__(self, _("Add _Link..."))
        self.rich_entry = rich_entry
        self.connect("clicked", self._onClicked)

    def _onClicked(self, button):
        dialog = gtk.Dialog(_("Add Link"), buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                                                       _("_Add Link"), gtk.RESPONSE_ACCEPT))
        
        dialog.set_default_response(gtk.RESPONSE_ACCEPT)
        dialog.set_has_separator(gtk.FALSE)
        dialog.set_resizable(gtk.FALSE)
        dialog.set_border_width(5)
        dialog.vbox.set_spacing(2)
        
        textLabel = gtk.Label(_("Text:"))
        textLabel.set_alignment(0.0, 0.5)

        urlLabel = gtk.Label(_("URL:"))
        urlLabel.set_alignment(0.0, 0.5)

        textEntry = gtk.Entry()            
        urlEntry  = gtk.Entry()
        urlEntry.set_activates_default(gtk.TRUE)

        selection = self.rich_entry.buffer.get_selection_bounds()

        if selection:
            textEntry.set_text(self.rich_entry.buffer.get_text(selection[0],selection[1]))

        table = gtk.Table(rows=2, columns=2)
        table.set_border_width(5)
        
        table.set_row_spacings(6)
        table.set_col_spacings(12)

        table.attach(textLabel, 0, 1, 0, 1, xoptions=gtk.FILL)
        table.attach(urlLabel, 0, 1, 1, 2, xoptions=gtk.FILL)
        table.attach(textEntry, 1, 2, 0, 1)
        table.attach(urlEntry, 1, 2, 1, 2)

        dialog.vbox.pack_start(table)

        table.show_all()

        if selection:
            urlEntry.grab_focus()
        else:
            textEntry.grab_focus()

        response = dialog.run()

        if response == gtk.RESPONSE_ACCEPT:
            if selection:
                self.rich_entry.applyHyperlink(selection, urlEntry.get_text(), self._onHyperlinkClicked)
            else:
                iter = self.rich_entry.buffer.get_iter_at_mark(self.rich_entry.buffer.get_mark("insert"))
                self.rich_entry.addHyperlink(iter, textEntry.get_text(), urlEntry.get_text(), self._onHyperlinkClicked)

        dialog.hide()
            
    def _onHyperlinkClicked(self, uri):
        print "Clicked %s" % (uri)
        
class StyleToggle(gtk.ToggleButton):
    def __init__(self, stock_icon_id, tag, htmltag, text_view):
        gtk.ToggleButton.__init__(self)

        tag.opening_tag = '<%s>' % (htmltag)
        tag.closing_tag = '</%s>' % (htmltag)

        self.style_tag = tag
        self.text_buffer = text_view.get_buffer()
        self.cursor_mark = self.text_buffer.get_mark("insert")
        
        self.connect("clicked", self._onStyleToggleActivate)
        
        image = gtk.Image()
        image.set_from_stock(stock_icon_id, gtk.ICON_SIZE_SMALL_TOOLBAR)
        self.add(image)
        image.show()

        self.text_buffer.connect("mark-set", self._onMarkSet)

    def _onStyleToggleActivate(self, toggle):
        if self.programmatic_toggle:
            return
        
        selection = self.text_buffer.get_selection_bounds()
        
        if selection:
            # There's a selection, apply/remove style tag to it
            
            if self.get_active():
                self.text_buffer.apply_tag(self.style_tag, selection[0], selection[1])
            else:
                self.text_buffer.remove_tag(self.style_tag, selection[0], selection[1])
                    
    def _onMarkSet(self, textbuffer, iter, mark):
        if mark == self.cursor_mark:
            
            self.programmatic_toggle = gtk.TRUE
            if iter.has_tag(self.style_tag):
                self.set_active(gtk.TRUE)
            else:
                self.set_active(gtk.FALSE)
            self.programmatic_toggle = gtk.FALSE
