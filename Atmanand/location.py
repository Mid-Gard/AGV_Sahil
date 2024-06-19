from dronekit import connect, VehicleMode
import math
import json
import requests
import time

# Connect to the drone
vehicle = connect('/dev/ttyUSB0', wait_ready=True, baud=57600)

# Define the server URL
SERVER_URL = 'http://192.168.0.186:8000/agv_rover/loc_post/'

def send_location_data(latitude, longitude, pitch, roll, yaw):
    data = {
        'lat': latitude,
        'lon': longitude,
        'pitch': pitch,
        'roll': roll,
        'yaw': yaw
    }
    agvloc_data = json.dumps({'agvlocdata': data})
    print(agvloc_data)
    try:
        response = requests.post(SERVER_URL, json=agvloc_data)
        if response.status_code == 200:
            print("Location data sent successfully")
        else:
            print(f"Error sending location data: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending location data: {e}")

@vehicle.on_message('GPS_RAW_INT')
def gps_listener(self, name, message):
    lat = message.lat * 1e-7
    lon = message.lon * 1e-7
    send_location_data(lat, lon, pitch, roll, yaw)

@vehicle.on_message('ATTITUDE')
def attitude_listener(self, name, message):
    global pitch, roll, yaw
    pitch = (math.degrees(message.pitch)+ 360) % 360
    roll = (math.degrees(message.roll)+ 360) % 360
    yaw = (math.degrees(message.yaw) + 360) % 360
    print(f"Pitch: {pitch}, Roll: {roll}, Yaw: {yaw}")

# Initialize global variables
pitch = 0
roll = 0
yaw = 0

if __name__ == "__main__":
    try:
        while True:
            # Update GPS and attitude data
            lat = vehicle.location.global_frame.lat
            lon = vehicle.location.global_frame.lon
            send_location_data(lat, lon, pitch, roll, yaw)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        vehicle.close()
