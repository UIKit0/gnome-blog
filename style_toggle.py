import gtk

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
