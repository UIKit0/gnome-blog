import gconf

class FeatureNotSupported(Exception):
    def __init__(self, unknownMethod):
        Exception.__init__(self, "Blog protocol does not support '%s'" % (unknownMethod))
        
def getBlogList (gconf_prefix):
    client = gconf.client_get_default()
    username, password, protocol, url = _getSettings(client, gconf_prefix)
    blog_backend = _getBlogBackend(protocol)
    
    try:
        return blog_backend.getBlogList(username, password, url, client, gconf_prefix)
    except AttributeError, e:
        raise FeatureNotSupported("getBlogList")

    
def postEntry (title, entry, gconf_prefix, keywords):
    client = gconf.client_get_default()
    username, password, protocol, url = _getSettings(client, gconf_prefix)
    blog_backend = _getBlogBackend(protocol)
          
    return blog_backend.postEntry(username, password,
                                  url, title, entry,
				  keywords,
                                  client, gconf_prefix)
        
def uploadImage (image, gconf_prefix):
    client = gconf.client_get_default()
    username, password, protocol, url = _getSettings(client, gconf_prefix)
    blog_backend = _getBlogBackend(protocol)

    try:
        imageurl = blog_backend.uploadImage(username, password,
                                            url,
                                            image.name,
                                            image.file_contents,
                                            image.mime_type,
                                            client, gconf_prefix)
        if imageurl == None:
            raise FeatureNotSupported("uploadImage")
    except AttributeError, e:
        raise FeatureNotSupported("uploadImage")
    
    return imageurl

def _getSettings(client, gconf_prefix):
    print "Using prefix %s" % (gconf_prefix)
    username = client.get_string(gconf_prefix + "/blog_username")
    password = client.get_string(gconf_prefix + "/blog_password")
    protocol = client.get_string(gconf_prefix + "/blog_protocol")
    url      = client.get_string(gconf_prefix + "/xmlrpc_url")

    return username, password, protocol, url

def _getBlogBackend(protocol):
    modulename = "gnomeblog.%s" % (protocol)
    protocolModule = __import__(modulename, globals(), locals(), ['blog'])
    return protocolModule.blog
