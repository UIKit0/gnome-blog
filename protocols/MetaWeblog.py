import xmlrpclib
import base64

from gtk import TRUE, FALSE
import gconf

import gettext
_ = gettext.gettext

from gnomeblog import hig_alert
from gnomeblog import bloggerAPI

class Blog(bloggerAPI.Blog):
    def __init__(self):
        bloggerAPI.Blog.__init__(self)

    def postEntry (self, username, password, base_url, title,
                   entry, client, gconf_prefix):

        url = self._getURL(base_url, client, gconf_prefix)

        if (base_url == None):
            hig_alert.reportError("Could not post Blog entry", "No XML-RPC server URL to post blog entries to is set, or the value could not be retrieved from GConf. Your entry will remain in the blogger window.")
            return FALSE

        blog_id  = client.get_string(gconf_prefix + "/blog_id")

        success = TRUE

        server = xmlrpclib.Server(url)

        content = {}
        content['title'] = title
        content['description'] = entry

        try:
            server.metaWeblog.newPost(blog_id, username, password, content, xmlrpclib.True)
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, "Could not post blog entry", username, blog_id, url)
            success = FALSE
        except xmlrpclib.ProtocolError, e:
            hig_alert.reportError("Could not post Blog entry", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: %s.' % (url, hig_alert.italic(e.errmsg)))
            success = FALSE

        return success

    def uploadImage (self, username, password, base_url,
                     file_name, file_contents, mime_type, client, gconf_prefix):

        url = self._getURL(base_url, client, gconf_prefix)

        blog_id  = client.get_string(gconf_prefix + "/blog_id")

        success = TRUE
        
        server = xmlrpclib.Server(url)

        content = {}
        content['name'] = filename
        content['type'] = mime_type
        content['bits'] = base64.encodestring(file_contents)

        try:
            server.metaWeblog.newMediaObject(blog_id, username, password, content)
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, "Could not post Image", username, blog_id, url)
            success = FALSE
        except xmlrpclib.ProtocolError, e:
            hig_alert.reportError("Could not post Blog entry", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: %s.' % (url, hig_alert.italic(e.errmsg)))
            success = FALSE
            
blog = Blog()
