import gconf

def getBlogList (gconf_prefix):
    client = gconf.client_get_default()
    username, password, protocol, url = _getSettings(client, gconf_prefix)
    blog_backend = _getBlogBackend(protocol)

    return blog_backend.getBlogList(username, password, url, client, gconf_prefix)

    
def postEntry (title, entry, gconf_prefix):
    client = gconf.client_get_default()
    username, password, protocol, url = _getSettings(client, gconf_prefix)
    blog_backend = _getBlogBackend(protocol)
          
    return blog_backend.postEntry(username, password,
                                  url, title, entry,
                                  client, gconf_prefix)
        

def _getSettings(client, gconf_prefix):
    print "Using prefix %s" % (gconf_prefix)
    username = client.get_string(gconf_prefix + "/blog_username")
    password = client.get_string(gconf_prefix + "/blog_password")
    protocol = client.get_string(gconf_prefix + "/blog_protocol")
    url      = client.get_string(gconf_prefix + "/xmlrpc_url")

    return username, password, protocol, url

def _getBlogBackend(protocol):
    modulename = "gnomeblog.%s" % (protocol)
    print "Getting module %s" % modulename
    protocolModule = __import__(modulename, globals(), locals(), ['blog'])
    return protocolModule.blog
