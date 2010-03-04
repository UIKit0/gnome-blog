import xmlrpclib
import base64

import gconf


import gettext
_ = gettext.gettext

from gnomeblog import hig_alert
from gnomeblog import bloggerAPI
from gnomeblog import proxy
from gnomeblog import blog

class Blog(bloggerAPI.Blog):
    def __init__(self):
        bloggerAPI.Blog.__init__(self)

    def postEntry (self, username, password, base_url, title,
                   entry, keywords, client, gconf_prefix):

        url = self._getURL(base_url, client, gconf_prefix)

        if (base_url == None):
            hig_alert.reportError("Could not post Blog entry", "No XML-RPC server URL to post blog entries to is set, or the value could not be retrieved from GConf. Your entry will remain in the blogger window.")
            return False

        blog_id  = client.get_string(gconf_prefix + "/blog_id")

        success = True

        #check for GNOME proxy configurations and use if required
        proxy_transport = proxy.GnomeProxyTransport(client)
        server = proxy_transport.get_server(url);

        content = {}
        content['title'] = title
        content['description'] = entry
	content['mt_keywords'] = keywords

        try:
            server.metaWeblog.newPost(blog_id, username, password, content, xmlrpclib.True)
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, "Could not post blog entry", username, blog_id, url)
            success = False
        except xmlrpclib.ResponseError, e:
            hig_alert.reportError("Could not post Blog entry", 'Received an invalid response: %s posting to URL %s.' % (hig_alert.italic(e), url))
            success = False
        except xmlrpclib.ProtocolError, e:
            hig_alert.reportError("Could not post Blog entry", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: %s.' % (url, hig_alert.italic(e.errmsg)))
            success = False

        return success

    def uploadImage (self, username, password, base_url,
                     file_name, file_contents, mime_type, client, gconf_prefix):

        url = self._getURL(base_url, client, gconf_prefix)

        blog_id  = client.get_string(gconf_prefix + "/blog_id")

        success = True
        
        #check for GNOME proxy configurations and use if required
        proxy_transport = proxy.GnomeProxyTransport(client)
        server = proxy_transport.get_server(url); 

        content = {}
        content['name'] = file_name
        content['type'] = mime_type
        content['bits'] = xmlrpclib.Binary(file_contents)

        imageurl = None

        try:
            imageurl = (server.metaWeblog.newMediaObject(blog_id, username, password, content))['url']
        except xmlrpclib.Fault, e:
            hig_alert.handleBloggerAPIFault(e, "Could not post Image", username, blog_id, url)
        except xmlrpclib.ProtocolError, e:
            hig_alert.reportError("Could not post Blog entry", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: %s.' % (url, hig_alert.italic(e.errmsg)))

        return imageurl
    
blog = Blog()
