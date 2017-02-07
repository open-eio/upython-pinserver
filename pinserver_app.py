################################################################################
# STANDARD LIB IMPORTS
import os, time
try:
    from collections import OrderedDict
except ImportError:
    from ucollections import OrderedDict #micropython specific
    
try:
    import machine
except ImportError:
    import mock_machine as machine #a substitute for PC testing
    
try:
    import json
except ImportError:
    import ujson as json #micropython specific

#-------------------------------------------------------------------------------
# PAWPAW PACKAGE IMPORTS
from pawpaw import WebApp, route, Template, LazyTemplate

#-------------------------------------------------------------------------------
# LOCAL IMPORTS

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

SERVER_ADDR = app.cfg.get('server_addr','0.0.0.0')  #default to localhost on PC
SERVER_ADDR = app.cfg.get('server_port',9999)

################################################################################
# GLOBALS
#-------------------------------------------------------------------------------
PIN_NUMBERS = (0, 2, 4, 5, 12, 13, 14, 15)
PINS = OrderedDict((i,machine.Pin(i, machine.Pin.IN)) for i in PIN_NUMBERS)

################################################################################
# APPLICATION CODE
#-------------------------------------------------------------------------------
class PinServer(WebApp):
    @route("/", methods=['GET','POST'])
    def pins(self, context):
        if DEBUG:
            print("INSIDE ROUTE HANDLER name='%s' " % ('pins'))
        
        #open the template files
        pins_tmp   = LazyTemplate.from_file("templates/pins.html_template")
        ptr_tmp    =     Template.from_file("templates/pins_table_row.html_template")
        pins_jstmp = LazyTemplate.from_file("templates/pins.js_template")
        comment = ""
        
        if context.request.method == 'POST':
            if DEBUG:
                print("HANDLING POST REQUEST: args = %r" % context.request.args)
            #get the button id from the params and pull out the corresponding pin object
            btn_id = context.request.args['btn_id']
            pin_id = int(btn_id[3:])#pattern is "btn\d\d"
            pin = PINS[pin_id]
            pin.value = not pin.value() #invert the pin state
            comment = "Toggled pin %d" % pin_id
        
        #we make table content a generator that produces one row per iteration
        def gen_table_content(pins):
            for pin_num, pin in pins.items():
                ptr_tmp.format(pin_id = str(pin),
                               pin_value = 'HIGH' if pin.value() else 'LOW',
                              )
                for line in ptr_tmp.render():
                    yield line
        
        server_base_url = "%s:%s" % (self.server_addr,self.server_port)
        pins_jstmp.format(server_base_url = server_base_url)
        pins_tmp.format(table_content = gen_table_content(PINS),
                        comment=comment,
                        javascript = pins_jstmp)
        #finally render the view
        context.render_template(pins_tmp)
        
################################################################################
# MAIN
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    #---------------------------------------------------------------------------
    # Create application instance binding to localhost on port 9999
    app = PinServer(server_addr = SERVER_ADDR,
                    server_port = SERVER_PORT,
                   )

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    app.serve_forever()
