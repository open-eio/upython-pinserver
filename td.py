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
        #add the method to the handler_registry with path as key
        for req_method in self.req_methods:
            key = "%s %s" % (req_method, self.path)
            if DEBUG:
                print("@route REGISTERING HANDLER '%s' on method `%r`" % (key,m))
            self.registered_routes[key] = m
        return m

#a class decorator which creates a class-private Routing HttpRequestHandler
def Router(cls):
    if DEBUG:
        print("@Router: wrapping class '%s'" % cls)
        
    #this is a private class allowing independence of wrapped WebApp classes
    class RoutingRequestHandler(HttpRequestHandler):
        pass

    class RouterWrapped(cls):
        #update the private class to contain all currently registered routes
        _handler_registry = route.registered_routes.copy()
        def __init__(self,*args,**kwargs):
            if not kwargs.get("MyHttpRequestHandler") is None:
                print("Warning: @Router will overwrite 'MyHttpRequestHandler'")
            #bind self to all of the route handlers
            for key, handler in type(self)._handler_registry.items():
                RoutingRequestHandler.handler_registry[key] = lambda context: handler(self,context)
            kwargs['MyHttpRequestHandler'] = RoutingRequestHandler
            cls.__init__(self,*args, **kwargs)
    
    #remove the registered_routes from the route decorator class 
    #attribute space, this allows for independent routing WebApp instances
    route.registered_routes = OrderedDict()
    return RouterWrapped

################################################################################
# Classes
class WebApp(object):
    def __init__(self, server_addr, server_port, MyHttpRequestHandler = None):
        if MyHttpRequestHandler is None:
            MyHttpRequestHandler = HttpRequestHandler #default handler
        # Create the server, binding to localhost on port 9999
        self.server_addr = server_addr
        self.server_port = server_port
        self._MyHttpRequestHandler = MyHttpRequestHandler
        self._server = TCPServer((self.server_addr, self.server_port), MyHttpRequestHandler)
        
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

