import xmlrpclib

import gtk
import gconf

import hig_alert

appkey = "6BF507937414229AEB450AB075001667C8BC8338"

def postEntry (title, entry, gconf_prefix):
    client = gconf.client_get_default()

    print ("GConf_prefix is ", gconf_prefix)
    
    username = client.get_string(gconf_prefix + "/blog_username")
    password = client.get_string(gconf_prefix + "/blog_password")
    protocol = client.get_string(gconf_prefix + "/blog_protocol")
    url      = client.get_string(gconf_prefix + "/xmlrpc_url")

    if (protocol == "bloggerAPI"):
        successful_post = _postEntryBloggerAPI(username, password,
                                               url, title, entry,
                                               client, gconf_prefix)
    elif (protocol == "advogato"):
        successful_post = _postEntryAdvogato(username, password,
                                             url, title, entry,
                                             client, gconf_prefix)

    return successful_post
        
def _postEntryAdvogato (username, password, url, title, entry, client, gconf_prefix):
    server = xmlrpclib.Server(url)

    try:
      cookie = server.authenticate(username, password)
    except xmlrpclib.Fault, e:
      if (server.user.exists (username) == 0):
        hig_alert.reportError("Could not post Blog entry", "Your username is invalid. Please double-check the preferences.")
	return gtk.FALSE
      else:
        hig_alert.reportError("Could not post Blog entry", "Your username or password is invalid. Please double-check the preferences.")
        return gtk.FALSE

    success = gtk.TRUE

    try:
      server.diary.set(cookie, -1, entry)

    except xmlrpclib.Fault, e:
      hig_alert.handleBloggerAPIFault(e, "Could not post blog entry", username, blog_id, url)
      success = gtk.FALSE
    except xmlrpclib.ProtocolError, e:
      hig_alert.reportError("Could not post Blog entry", 'URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: <span style=\"italic\">%s</span>.' % (url, e.errmsg))
      success = gtk.FALSE

    print ("Success is....")
    print (success)

    return success

def _postEntryBloggerAPI (username, password, url, title, entry, client, gconf_prefix):
    global appkey
    
    if (url == None):
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
