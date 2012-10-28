import socket
import atom
import gdata
from gdata import service;

import gconf

import gettext
_ = gettext.gettext

from gnomeblog import hig_alert
from gnomeblog import proxy

class Blog:
    def __init__(self):
        pass
    
    def _getURL(self, base_url, client, gconf_prefix):
        url_ending = client.get_string (gconf_prefix + "/url_ending")
        return base_url + url_ending
    
    def getBlogList(self, username, password, base_url, client, gconf_prefix):
        # TODO: consider GNOME proxy configurations, as in bloggerAPI.py
        error_name = _("Could not get list of blogs.")
        
        try:
            blogger_service = self._login (username, password)
        except service.CaptchaRequired as message:
            hig_alert.reportError (error_name, _("A CAPTCHA was required for authentication.")) # TODO: propagadate captcha
            return None
        except service.BadAuthentication as message:
            hig_alert.reportError (error_name, _("Username or password was invalid."))
            return None
        except service.Error as message:
            hig_alert.reportError (error_name, _("Failed to login: %s" % message))
            return None
        except socket.gaierror as message:
            hig_alert.reportError (error_name, _("Socket error: %s.  Perhaps try again." % message));
            return None

        blog_list = blogger_service.Get ('/feeds/default/blogs'); # is there anyway to sort these by recently used?

        if ((blog_list.entry == None) or (len(blog_list.entry) == 0)):
            # No blogs found
            hig_alert.reportError (_("No Blogs Found"), _("No errors were reported, but no blogs were found at %s for %s\n" % (url, username)));

        string_value_pairs = []

        for blog in blog_list.entry:
            blog_title = blog.title.text
            blog_id = blog.id.text.split ('-')[-1]
            string_value_pairs.append ( (blog_title, blog_id) );

        return string_value_pairs

    def _login (self, username, password):
        if username.endswith ('@gmail.com') == False: # can use blogger with a non-Gmail address? 
            username = username + "@gmail.com";

        service = gdata.service.GDataService (username, password)
        service.source = "Gnome Blog"
        service.service = "blogger"
        service.server = "www.blogger.com"
        service.ProgrammaticLogin ()

        return service
    
    def postEntry (self, username, password, base_url, title, entry, keywords, client, gconf_prefix):
        blog_id = client.get_string (gconf_prefix + "/blog_id");

        if (blog_id == None):
            blog_id = ""

        if (username == None):
            username = ""

        if (password == None):
            password = ""

        url = self._getURL(base_url, client, gconf_prefix)

        # consider GNOME proxy configuration, but perhaps python's gdata lib does that? 

        post = gdata.GDataEntry ()
        post.title = atom.Title (title_type = 'xhtml', text = title)
        post.content = atom.Content (content_type = 'html', text = entry)
        
        if keywords is not None and keywords != "":
            scheme = "http://www.blogger.com/atom/ns#"
            for keyword in keywords.split (","):
                post.category.append (atom.Category (keyword, scheme))
            
        success = True

        error_name = _("Could not post entry.")
        try:
            blogger_service = self._login (username, password)
        except service.CaptchaRequired as message:
            hig_alert.reportError (error_name, _("A captcha was required for authentication.")) # TODO; propagate it
            success = False
        except service.BadAuthentication as message:
            hig_alert.reportError (error_name, _("Username or password was invalid."))
            success = False
        except service.Error as message:
            hig_alert.reportError (error_name, _("Failed to login: %s" % message))
            success = False
        except socket.gaierror as message:
            hig_alert.reportError (error_name, _("Socket error: %s.  Perhaps try again." % message));
            success = False

        if success == True:
            try:
                blogger_service.Post (post, "/feeds/%s/posts/default" % blog_id)
            except service.RequestError as message:
                hig_alert.reportError (error_name, _("Failed to post: %s" % message['body']))

        return success

blog = Blog()
