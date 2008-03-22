import xmlrpclib

import gconf

import gettext
_ = gettext.gettext

from gnomeblog import hig_alert
from gnomeblog import proxy

appkey = "6BF507937414229AEB450AB075001667C8BC8338"

class Blog:
    def __init__(self):
        pass

    def _getURL(self, base_url, client, gconf_prefix):
        url_ending = client.get_string (gconf_prefix + "/url_ending")
        return base_url + url_ending

    def getBlogList(self, username, password, base_url, client, gconf_prefix):
        global appkey
        
        url = self._getURL(base_url, client, gconf_prefix)

        print ("Getting list for RPC interface %s" % (url))
        
        #check for GNOME proxy configurations and use if required
        proxy_transport = proxy.GnomeProxyTransport(client)
        server = proxy_transport.get_server(url); 

        try:
            bloglist = server.blogger.getUsersBlogs(appkey, username, password)
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, _("Could not get list of blogs"), username, None, url)
            return
        except xmlrpclib.ProtocolError, e:            
            hig_alert.reportError(_("Could not get list of blogs"), _('URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: %s.') % (url, hig_alert.italic(e.errmsg)))
            return

        if ((bloglist == None) or (len(bloglist) == 0)):
            # No blogs found!
            hig_alert.reportError("No Blogs Found", "No errors were reported, but no blogs were found at %s for username %s\n" % ( url, username))
            return

        string_value_pairs = []

        for blog in bloglist:
            string_value_pairs.append((blog["blogName"], blog["blogid"]))

        return string_value_pairs



    def postEntry (self, username, password, base_url, title, entry, keywords, client, gconf_prefix):
        global appkey

        url = self._getURL(base_url, client, gconf_prefix)
        
        if (base_url == None):
            hig_alert.reportError(_("Could not post Blog entry"), _("No XML-RPC server URL to post blog entries to is set, or the value could not be retrieved from GConf. Your entry will remain in the blogger window."))
            return False

        blog_id  = client.get_string(gconf_prefix + "/blog_id")

        if (blog_id == None):
            blog_id = ""

        if (username == None):
            username = ""

        if (password == None):
            password = ""
            
        content = title + "\n" + entry
        success = True

        #check for GNOME proxy configurations and use if required
        proxy_transport = proxy.GnomeProxyTransport(client)
        server = proxy_transport.get_server(url); 

        try:
            server.blogger.newPost(appkey, blog_id, username, password,
                                   content, xmlrpclib.True)
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, _("Could not post blog entry"), username, blog_id, url)
            success = False
        except xmlrpclib.ProtocolError, e:
            hig_alert.reportError(_("Could not post Blog entry"), _('URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: %s.') % (url, hig_alert.italic(e.errmsg)))
            success = False

        print ("Success is....")
        print (success)

        return success

blog = Blog()
