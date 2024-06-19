from dronekit import connect, VehicleMode
import math
import json
vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=57600)

@vehicle.on_message('GPS_RAW_INT')
def gps_listener(self, name, message):
    print("Latitude:", message.lat, "Longitude:", message.lon)

@vehicle.on_message('ATTITUDE')
def attitude_listener(self, name, message):
    pitch=math.degrees(message.pitch)
    roll =math.degrees(message.roll)
    yaw = math.degrees(message.yaw)
    yaw_deg = (yaw + 360) % 360
    print( "pitch" , pitch ,"roll" ,roll ,"Yaw (degrees):", yaw_deg)

while True:
    pass
if __name__ == "__main__":
    main()