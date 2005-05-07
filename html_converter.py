import gtk

def getHTML(buffer):
    global para_tag
    
    next_iter = buffer.get_start_iter()

    open_tags = [ para_tag ]
    html = "<p>" + _getTagsHTML(next_iter, open_tags)

    while not next_iter.is_end():
        iter = next_iter
        next_iter = _getNextIter(iter)

        new_text = buffer.get_text(iter, next_iter, True)
        html = html + new_text + _getTagsHTML(next_iter, open_tags)

    return html.decode('utf8')

  
def _getNextIter(iter):
    nextTagIter  = iter.copy()
    endLineIter  = iter.copy()

    tagFound = nextTagIter.forward_to_tag_toggle(None)
    endLineIter.forward_to_line_end()

    position = nextTagIter.compare(endLineIter)

    if tagFound and position == -1:
        print ("Iter is for tag")
        next_iter = nextTagIter
    else:
        print ("Iter is for endline")
        next_iter = endLineIter

    return next_iter

def _getTags(iter):
    global para_tag
    
    turnontags  = iter.get_toggled_tags(True)
    turnofftags = iter.get_toggled_tags(False)

    if iter.is_end():
        # Iter is at the end of the buffer
        turnofftags.append(para_tag)
    elif iter.ends_line():
        turnofftags.append(para_tag)
        turnontags.insert(0, para_tag)
        
    return turnofftags, turnontags

def _getTagsHTML(iter, open_tags):
    (turnofftags, turnontags) = _getTags(iter)

    html = ""
    
    html = html +  _turnOffTags(turnofftags, open_tags)
    html = html + _turnOnTags(turnontags, open_tags)

    return html

def _turnOnTags(turnontags, open_tags):
    html = ""
    for tag in turnontags:
        open_tags.append(tag)
        html = html + tag.opening_tag
    return html

def _turnOffTags(turnofftags, open_tags):
    html = ""
    for tag in turnofftags:
        tags_to_reopen = []
        opentag = open_tags.pop()
        while opentag != tag:
            html = html + opentag.closing_tag
            tags_to_reopen.append(opentag)
            opentag = open_tags.pop()

        html = html + tag.closing_tag
        html = html + _turnOnTags(tags_to_reopen, open_tags)

    return html

