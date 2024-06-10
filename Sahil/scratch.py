import serial
import json
import time
import math
from dronekit import connect, VehicleMode
import math

vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=57600)

@vehicle.on_message('GPS_RAW_INT')
def listener(self, name, message):
    print("Latitude:", message.lat, "Longitude:", message.lon)
    return