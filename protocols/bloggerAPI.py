import xmlrpclib

import gtk
import gconf

from gnomeblog import hig_alert

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
        
        server = xmlrpclib.Server(url)

        try:
            bloglist = server.blogger.getUsersBlogs(appkey, username, password)
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, "Could not get list of blogs", username, None, url)
            return
        except xmlrpclib.ProtocolError, e:            
            hig_alert.reportError("Could not get list of blogs", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: <span style=\"italic\">%s</span>.' % (url, e.errmsg))
            return

        if ((bloglist == None) or (len(bloglist) == 0)):
            # No blogs found!
            hig_alert.reportError("No Blogs Found", "No errors were reported, but no blogs were found at %s for username %s\n" % ( url, username))
            return

        string_value_pairs = []

        for blog in bloglist:
            string_value_pairs.append((blog["blogName"], blog["blogid"]))

        return string_value_pairs



    def postEntry (self, username, password, base_url, title, entry, client, gconf_prefix):
        global appkey

        url = self._getURL(base_url)

        if (base_url == None):
            hig_alert.reportError("Could not post Blog entry", "No XML-RPC server URL to post blog entries to is set, or the value could not be retrieved from GConf. Your entry will remain in the blogger window.")
            return gtk.FALSE

        blog_id  = client.get_string(gconf_prefix + "/blog_id")


        content = title + "\n" + entry
        success = gtk.TRUE

        server = xmlrpclib.Server(url)

        try:
            server.blogger.newPost(appkey, blog_id, username, password,
                                   content, xmlrpclib.True)
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, "Could not post blog entry", username, blog_id, url)
            success = gtk.FALSE
        except xmlrpclib.ProtocolError, e:
            hig_alert.reportError("Could not post Blog entry", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: <span style=\"italic\">%s</span>.' % (url, e.errmsg))
            success = gtk.FALSE

        print ("Success is....")
        print (success)

        return success

blog = Blog()
