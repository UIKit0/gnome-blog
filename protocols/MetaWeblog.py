import xmlrpclib

import gtk
import gconf

from gnomeblog import hig_alert
from gnomeblog import bloggerAPI

appkey = "6BF507937414229AEB450AB075001667C8BC8338"

class Blog(bloggerAPI.Blog):
    def __init__(self):
        bloggerAPI.Blog.__init__(self)

    def postEntry (self, username, password, base_url, title, entry, client, gconf_prefix):
        global appkey

        url = self._getURL(base_url, client, gconf_prefix)

        if (base_url == None):
            hig_alert.reportError("Could not post Blog entry", "No XML-RPC server URL to post blog entries to is set, or the value could not be retrieved from GConf. Your entry will remain in the blogger window.")
            return gtk.FALSE

        blog_id  = client.get_string(gconf_prefix + "/blog_id")

        success = gtk.TRUE

        server = xmlrpclib.Server(url)

        content = {}
        content['title'] = title
        content['description'] = entry

        try:
            server.metaWeblog.newPost(blog_id, username, password, content, xmlrpclib.True)
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, "Could not post blog entry", username, blog_id, url)
            success = gtk.FALSE
        except xmlrpclib.ProtocolError, e:
            hig_alert.reportError("Could not post Blog entry", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: <span style=\"italic\">%s</span>.' % (url, e.errmsg))
            success = gtk.FALSE

        return success

blog = Blog()
