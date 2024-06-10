import io
import time
import cv2
import numpy as np
import serial
import time
import json
from dronekit import connect, VehicleMode
import math
import requests


agv_url= 'http://192.168.0.186:8000/agv_rover/data_post/'
agv_url1= 'http://192.168.0.186:8000/agv_rover/battery_post/'
headersList = {
    'Accept': '/',
    'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
    'Content-Type': 'application/json'
}
vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=57600)
def main():
    gps_data = None
    attitude_data = None

    @vehicle.on_message('GPS_RAW_INT')
    def gps_listener(self, name, message):
        nonlocal gps_data
        gps_data = {'latitude': message.lat, 'longitude': message.lon}

    @vehicle.on_message('ATTITUDE')
    def attitude_listener(self, name, message):
        nonlocal attitude_data
        roll_deg = math.degrees(message.roll)
        pitch_deg = math.degrees(message.pitch)
        yaw_deg = math.degrees(message.yaw)
        attitude_data = {'roll_degrees': roll_deg, 'pitch_degrees': pitch_deg, 'yaw_degrees': yaw_deg}

    try:
        while True:
            if gps_data is not None and attitude_data is not None:
                combined_data = {**gps_data, **attitude_data}  # Combine both dictionaries
                combined_json = json.dumps(combined_data)
                print(combined_json)
                response = requests.post(agv_url, data=json.dumps({'Movement_data': combined_json}), headers=headersList)
                # Reset the variables for the next iteration
                gps_data = None
                attitude_data = None
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated by user.")



if __name__ == '__main__':
    try:
        main()
    finally:
       pass
