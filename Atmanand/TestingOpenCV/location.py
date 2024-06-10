import serial
import pynmea2
import requests
import random
import time
import json

def read_coordinates():
    # serial_port = '/dev/ttyAMA2'
    # with serial.Serial(serial_port, 38400, timeout=1) as ser:
    #     while True:
            # raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
            
            # if raw_data.startswith('$GNRMC'):
            #     try:
            #         msg = pynmea2.parse(raw_data)
            #         latitude = "{:.5f}".format(msg.latitude)
            #         longitude = "{:.5f}".format(msg.longitude)
            #         print(f"Latitude: {latitude}, Longitude: {longitude}")
                    
            #         # Send location data to Django server
            #         send_location_data(latitude, longitude)
                    
            #     except KeyboardInterrupt:
            #         pass
            
    while True:
        # Testing with dummy data, use above code to use GPS
        try:
            latitude = random.uniform(30,70)
            longitude = random.uniform(30,70)
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            
            # Send location data to Django server
            send_location_data(latitude, longitude)
            time.sleep(1)
        except KeyboardInterrupt:
            pass

def send_location_data(latitude, longitude):
    SERVER_URL = 'http://192.168.0.186:8000/agv_rover/loc_post/'
    data = {
        'lat': latitude,
        'lon': longitude
    }
    agvloc_data = json.dumps({'agvlocdata': data})
    print(agvloc_data)
    try:
        # response = requests.post(SERVER_URL, json=agvloc_data)
        # response = requests.post(SERVER_URL, data={'agvlocdata': data})
        response = requests.post(SERVER_URL, data=agvloc_data)
        if response.status_code == 200:
            print("Location data sent successfully")
        else:
            print(f"Error sending location data: {response}")
    except requests.RequestException as e:
        print(f"Error sending location data: {e}")

if __name__ == "__main__":
    read_coordinates()
