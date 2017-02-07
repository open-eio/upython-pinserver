#!/bin/bash -x
ampy -p /dev/ttyUSB0 -b 115200 put SECRET_CONFIG.json
ampy -p /dev/ttyUSB0 -b 115200 put network_setup.py
ampy -p /dev/ttyUSB0 -b 115200 put time_manager.py
ampy -p /dev/ttyUSB0 -b 115200 put dump_logs.py
ampy -p /dev/ttyUSB0 -b 115200 put pinserver_app.py
ampy -p /dev/ttyUSB0 -b 115200 put main.py
ampy -p /dev/ttyUSB0 -b 115200 put boot.py
