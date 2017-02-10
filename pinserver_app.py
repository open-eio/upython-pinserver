################################################################################
# STANDARD LIB IMPORTS
import sys, os, time
try:
    from collections import OrderedDict
except ImportError:
    from ucollections import OrderedDict #micropython specific
    
try:
    import json
except ImportError:
    import ujson as json #micropython specific

#-------------------------------------------------------------------------------
# PAWPAW PACKAGE IMPORTS
from pawpaw import WebApp, route, Template, LazyTemplate
from pawpaw.web_app import Router

#-------------------------------------------------------------------------------
# LOCAL IMPORTS
DEBUG = True

if DEBUG:
    print("INSIDE MODULE name='%s' " % ('pinserver_app',))
    try:
        from micropython import mem_info #micropython specific
        mem_info()
    except ImportError:
        pass

try:
    import machine #micropython specific
except ImportError:
    import mock_machine as machine #a substitute for PC testing
    
################################################################################
# CONFIGURATION
#-------------------------------------------------------------------------------
#read the SECRET configuration file, NOTE this contains PRIVATE keys and 
#should never be posted online
CONFIG_FILENAME = "SECRET_CONFIG.json"

config = {}
if CONFIG_FILENAME in os.listdir():
    config = json.load(open(CONFIG_FILENAME,'r'))

#load configuration for this module
app_cfg = config.get('pinserver_app', {})
DEBUG   = app_cfg.get('debug', 0)

SERVER_ADDR = app_cfg.get('server_addr')
SERVER_PORT = app_cfg.get('server_port')

################################################################################
# PLATFORM SPECIFIC SETUP
#-------------------------------------------------------------------------------
PLATFORM = sys.platform
if DEBUG:
    print("DETECTED PLATFORM: %s" % PLATFORM)
# ------------------------------------------------------------------------------
# ESP8266
if PLATFORM == 'esp8266':
    if SERVER_ADDR is None:
        SERVER_ADDR = "192.168.4.1" #default to AP interface
        if DEBUG:
            print("DEFAULTING SERVER_ADDR to '%s'" % SERVER_ADDR)
    if SERVER_PORT is None:
        SERVER_PORT = 80            #default HTTP port
        if DEBUG:
            print("DEFAULTING SERVER_PORT to '%s'" % SERVER_PORT)
    # Network/Services setup
    import network_setup
    if DEBUG:
        print("RUNNING network_setup.do_connect:")
    sta_if, ap_if = network_setup.do_connect(**config['network_setup'])
    time.sleep(1.0)
   
# ------------------------------------------------------------------------------
# DEFAULT PLATFORM
else:
    if SERVER_ADDR is None:
        SERVER_ADDR = "0.0.0.0" #default to localhost
        if DEBUG:
            print("DEFAULTING SERVER_ADDR to '%s'" % SERVER_ADDR)
    if SERVER_PORT is None:
        SERVER_PORT = 8080      #alternate HTTP port
        if DEBUG:
            print("DEFAULTING SERVER_PORT to '%s'" % SERVER_PORT)
################################################################################
# GLOBALS
#-------------------------------------------------------------------------------
PIN_NUMBERS = (0, 2, 4, 5, 12, 13, 14, 15)
PINS = OrderedDict((i,machine.Pin(i, machine.Pin.OUT)) for i in PIN_NUMBERS)

################################################################################
# APPLICATION CODE
#-------------------------------------------------------------------------------
@Router
class PinServer(WebApp):
    @route("/", methods=['GET','POST'])
    def pins(self, context):
        global DEBUG
        if DEBUG:
            print("INSIDE ROUTE HANDLER name='%s' " % ('pins'))
            try:
                from micropython import mem_info
                mem_info()
            except ImportError:
                pass
        if context is None:
            context = self
        #open the template files
        pins_tmp   = LazyTemplate.from_file("templates/pins.html")
        ptr_tmp    =     Template.from_file("templates/pins_table_row.html")
        pins_jstmp = LazyTemplate.from_file("templates/pins.js")
        comment = ""
        
        if context.request.method == 'POST':
            if DEBUG:
                print("HANDLING POST REQUEST: req = %r" % context.request)
            #get the button id from the params and pull out the corresponding pin object
            btn_id = context.request.args['btn_id']
            pin_id = int(btn_id[3:])#pattern is "btn\d\d"
            pin = PINS[pin_id]
            pin.value(not pin.value()) #invert the pin state
            comment = "Toggled pin %d" % pin_id
        
        #we make table content a generator that produces one row per iteration
        def gen_table_content(pins):
            for pin_num, pin in pins.items():
                ptr_tmp.format(pin_id = pin_num,
                               pin_value = 'HIGH' if pin.value() else 'LOW',
                              )
                for line in ptr_tmp.render():
                    yield line
        
        #server_base_url = "%s:%s" % (self.server_addr,self.server_port)
        #pins_jstmp.format(server_base_url = server_base_url)
        pins_tmp.format(table_content = gen_table_content(PINS),
                        comment=comment,
                        javascript = pins_jstmp)
        #finally render the view
        context.render_template(pins_tmp)
        
        if DEBUG:
            print("LEAVING ROUTE HANDLER name='%s' " % ('pins'))
            try:
                from micropython import mem_info
                mem_info()
            except ImportError:
                pass
        
################################################################################
# MAIN
#-------------------------------------------------------------------------------
#if __name__ == "__main__":
#---------------------------------------------------------------------------
# Create application instance binding to localhost on port 9999
app = PinServer(server_addr = SERVER_ADDR,
                server_port = SERVER_PORT,
               )

# Activate the server; this will keep running until you
# interrupt the program with Ctrl-C
app.serve_forever()
