import xmlrpclib
import gconf

from xmlrpclib import Server, Transport

#This code is taken from BloGTK from code contributed by Michael Twomey <mick@enginesofcreation.ie>
#It has been modified by John (J5) Palmieri to add support for GNOME's proxy configuration 
                                                                                                                  
class GnomeProxyTransport(Transport):
    """Handles an HTTP transaction to an XML-RPC server, through an HTTP proxy."""
                                                                                                                  
    def __init__(self, client):
        base_key = "/system/http_proxy"
        host_key = base_key + "/host"
        port_key = base_key + "/port"
        use_proxy_key = base_key + "/use_http_proxy"
        use_authentication_key = base_key + "/use_authentication"
        user_key = base_key + "/authentication_user"
        pass_key = base_key + "/authentication_password"

        self.proxyHost = client.get_string(host_key) 
        self.proxyPort = client.get_int(port_key)
        self.useProxy = ( client.get_bool(use_proxy_key) and \
                          self.proxyHost != "" and \
                          self.proxyPort != 0 )
		
        #Authentication not yet supported 
        self.useAuthentication = client.get_bool(use_authentication_key)
        self.username = client.get_string(user_key) 
        self.password = client.get_string(pass_key) 
                                                                                                                  
    def request(self, host, handler, request_body, verbose=0):
        return Transport.request(self, host, "http://"+host+handler, request_body, verbose)
                                                                                                                  
    def make_connection(self, host):
        import httplib
        return httplib.HTTP(self.proxyHost, self.proxyPort)

    def use_proxy(self):
        return self.useProxy

    def get_server(self, url):
        server = ""
	
        if (self.useProxy):
            server = xmlrpclib.Server(url, transport=self, allow_none=True)
        else:
            server = xmlrpclib.Server(url, allow_none=True)

        return server;


if __name__ == "__main__":
    p = GnomeProxyTransport(gconf.client_get_default())
    print p.useProxy
    print p.proxyHost
    print p.proxyPort
    print p.useAuthentication
    print p.username
    print p.password
