import gtk
from gtk import gdk
import html_converter

class RichEntry(gtk.TextView):
    def __init__(self):
        self.buffer = gtk.TextBuffer()
        gtk.TextView.__init__(self, self.buffer)
        
        self.set_editable(gtk.TRUE)
        self.set_wrap_mode(gtk.WRAP_WORD)

        html_converter.para_tag = self.buffer.create_tag("p")
        html_converter.para_tag.opening_tag = "<p>"
        html_converter.para_tag.closing_tag = "</p>"

        self.connect("event-after", self._onEventAfter)

    def addHyperlink(self, iter, text, uri, on_activate):
        link_tag = self.buffer.create_tag()
        link_tag.set_property("underline", pango.UNDERLINE_SINGLE)
        link_tag.set_property("foreground", "#0000FF")
        
        link_tag.uri = uri
        link_tag.on_activate = on_activate
        link_tag.hyperlink = gtk.TRUE

        self.buffer.insert_with_tags(text, link_tag)

    def getHTML(self):
        return html_converter.getHTML(self.buffer)

    def clear(self):
        self.buffer.delete(self.buffer.get_start_iter(),
                           self.buffer.get_end_iter())

    def createStyleToggle(self, pango_markup_properties, stock_button, html_tag):
        tag = self.buffer.create_tag()
        for property in pango_markup_properties:
            tag.set_property(property[0], property[1])
        return StyleToggle(stock_button, tag, html_tag, self)
        
    def _onEventAfter(self, widget, event):
        if ((event.type != gdk.BUTTON_RELEASE) or (event.button != 1)):
            return gtk.FALSE

        bounds = self.buffer.get_selection_bounds()
        if (bounds == ()):
            return gtk.FALSE

        (x, y) = self.window_to_buffer_coords (gtk.TEXT_WINDOW_WIDGET, int(event.x), int(event.y))

        iter = self.get_iter_at_location(x, y)

        for tag in iter.get_tags():
            try:
                if (tag.hyperlink == gtk.TRUE):
                    # Found Hyperlink, activating
                    tag.on_activate(uri)
            except AttributeError:
                pass
            
        return gtk.FALSE
        
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
        if (self.programmatic_toggle == gtk.TRUE):
            return
        
        selection = self.text_buffer.get_selection_bounds()
        
        if (not selection == ()):
            # There's a selection, apply/remove style tag to it
            
            if (self.get_active()):
                self.text_buffer.apply_tag(self.style_tag, selection[0], selection[1])
            else:
                self.text_buffer.remove_tag(self.style_tag, selection[0], selection[1])
                    
    def _onMarkSet(self, textbuffer, iter, mark):
        if (mark == self.cursor_mark):
            
            self.programmatic_toggle = gtk.TRUE
            if (iter.has_tag(self.style_tag)):
                self.set_active(gtk.TRUE)
            else:
                self.set_active(gtk.FALSE)
            self.programmatic_toggle = gtk.FALSE
