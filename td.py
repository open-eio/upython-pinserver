import time
try:
    from collections import OrderedDict
except ImportError: 
    from ucollections import OrderedDict #micrpython specific

from pawpaw.socketserver    import TCPServer
from pawpaw.http_server     import HttpRequestHandler

DEBUG = True
################################################################################
# DECORATORS
#-------------------------------------------------------------------------------

#a method decorator to automate handling of HTTP route dispatching
class route(object):
    registered_routes = OrderedDict()

    def __init__(self, path, methods = None):
        #this runs upon decoration
        self.path = path
        if methods is None:
            methods = ["GET"]
        self.req_methods = methods
        
    def __call__(self, m):
        #this runs upon decoration immediately after __init__
        def wrapped_m(*args):
            return m(*args)
        #add the wrapped method to the handler_registry with path as key
        for req_method in self.req_methods:
            key = "%s %s" % (req_method, self.path)
            print("@route REGISTERING HANDLER '%s'" % (key,))
            self.registered_routes[key] = wrapped_m
        return wrapped_m

#a method decorator which creates a class-private Routing HttpRequestHandler
def Router(cls):
    class RoutingRequestHandler(HttpRequestHandler):
            pass    
    #update the private class to contain all currently registered routes
    RoutingRequestHandler.handler_registry = route.registered_routes.copy()
    #cache the private class
    cls._RoutingRequestHandler = RoutingRequestHandler
    #remove the registered_routes from the route decorator class 
    #attribute space, this allows for independent routing WebApp instances
    route.registered_routes = OrderedDict()
    return cls


        
################################################################################
# Classes
class WebApp(object):
    def __init__(self, server_addr, server_port):
        # Create the server, binding to localhost on port 9999
        self.server_addr = server_addr
        self.server_port = server_port
        #self._server = TCPServer((self.server_addr, self.server_port), self._RoutingRequestHandler)
        
    def serve_forever(self):
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        self._server.serve_forever()

################################################################################
# TEST  CODE
################################################################################
@Router
class App1(WebApp):
    @route("/11")
    def myhandler11(self,context):
        print("INSIDE App.myhandler")
    @route("/12")
    def myhandler12(self,context):
        print("INSIDE App.myhandler2")
@Router
class App2(WebApp):
    @route("/21")
    def myhandler21(self,context):
        print("INSIDE App.myhandler")
    @route("/22")
    def myhandler22(self,context):
        print("INSIDE App.myhandler2")

