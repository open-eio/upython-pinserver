#!/bin/bash -x
ampy -p /dev/ttyUSB0 -b 115200 put SECRET_CONFIG.json
ampy -p /dev/ttyUSB0 -b 115200 mkdir templates
ampy -p /dev/ttyUSB0 -b 115200 put ./templates/404.html /templates/404.html
ampy -p /dev/ttyUSB0 -b 115200 put ./templates/pins.html /templates/pins.html
ampy -p /dev/ttyUSB0 -b 115200 put ./templates/pins.js /templates/pins.js
ampy -p /dev/ttyUSB0 -b 115200 put ./templates/pins_table_row.html /templates/pins_table_row.html
ampy -p /dev/ttyUSB0 -b 115200 put network_setup.py
ampy -p /dev/ttyUSB0 -b 115200 put time_manager.py
ampy -p /dev/ttyUSB0 -b 115200 put dump_logs.py
ampy -p /dev/ttyUSB0 -b 115200 put pinserver_app.py
ampy -p /dev/ttyUSB0 -b 115200 put main.py
ampy -p /dev/ttyUSB0 -b 115200 put boot.py
