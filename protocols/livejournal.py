import xmlrpclib
import time

from gtk import TRUE, FALSE

import gettext
_ = gettext.gettext

from gnomeblog import hig_alert
from gnomeblog import gnome_blog_globals

appkey = "6BF507937414229AEB450AB075001667C8BC8338"
ver = 'GNOME-gnome-blog/' + gnome_blog_globals.version

class Blog:
    def __init__(self):
        pass

    def postEntry (self, username, password, url, title, entry, client, gconf_prefix):
        server = xmlrpclib.Server(url)
        info = {
          'username': username,
          'password': password,
          'clientversion': ver
        }

        try:
          cookie = server.LJ.XMLRPC.login(info)
        except xmlrpclib.Fault, e:
            hig_alert.reportError(_("Could not post Blog entry"), _("Your username or password is invalid. Please double-check the preferences."))
            return FALSE

        success = TRUE

        curtime = time.localtime()
        info = {
          'username': username,
          'password': password,
          'subject': title,
          'event': entry,
          'lineendings': 'unix',
          'year': curtime[0],
          'mon': curtime[1],
          'day': curtime[2],
          'hour': curtime[3],
          'min': curtime[4],
          'props': {
            'opt_preformatted': 1,
          }
        }

        try:
          server.LJ.XMLRPC.postevent(info)

        except xmlrpclib.Fault, e:
          hig_alert.handleBloggerAPIFault(e, _("Could not post blog entry"), username, username, url)
          success = FALSE
        except xmlrpclib.ProtocolError, e:
          hig_alert.reportError(_("Could not post Blog entry"), _('URL \'%s\' does not seem to be a valid LiveJournal XML-RPC server. Web server reported: %s.') % (url, hig_alert.italic(e.errmsg)))
          success = FALSE

        print ("Success is....")
        print (success)

        return success

blog = Blog()
