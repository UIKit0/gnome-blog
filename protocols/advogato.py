import xmlrpclib

import gtk

import gettext
_ = gettext.gettext

from gnomeblog import hig_alert

appkey = "6BF507937414229AEB450AB075001667C8BC8338"

class Blog:
    def __init__(self):
        pass

    def postEntry (self, username, password, url, title, entry, client, gconf_prefix):
        server = xmlrpclib.Server(url)

        try:
          cookie = server.authenticate(username, password)
        except xmlrpclib.Fault, e:
          if (server.user.exists (username) == 0):
            hig_alert.reportError(_("Could not post Blog entry"), _("Your username is invalid. Please double-check the preferences."))
            return gtk.FALSE
          else:
            hig_alert.reportError(_("Could not post Blog entry"), _("Your username or password is invalid. Please double-check the preferences."))
            return gtk.FALSE

        success = gtk.TRUE

        try:
          server.diary.set(cookie, -1, entry)

        except xmlrpclib.Fault, e:
          hig_alert.handleBloggerAPIFault(e, _("Could not post blog entry"), username, blog_id, url)
          success = gtk.FALSE
        except xmlrpclib.ProtocolError, e:
          hig_alert.reportError(_("Could not post Blog entry"), _('URL \'%s\' does not seem to be a valid bloggerAPI XML-RPC server. Web server reported: <span style=\"italic\">%s</span>.') % (url, e.errmsg))
          success = gtk.FALSE

        print ("Success is....")
        print (success)

        return success

blog = Blog()
