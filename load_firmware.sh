#!/bin/bash -x
esptool.py -p $1 --baud 460800 erase_flash
esptool.py -p $1 --baud 460800 write_flash --flash_size=detect 0 firmware-circuitpython-pawpaw.bin

