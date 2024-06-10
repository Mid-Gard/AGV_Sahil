import serial
import json
import time
import math
import pynmea2

def get_current_position(serial_port):
    with serial.Serial(serial_port, baudrate=38400, timeout=1) as ser_gps:
        while True:
            raw_data = ser_gps.readline().decode('utf-8',errors='ignore').strip()

            if raw_data.startswith('$GNRMC'):
                try:
                    msg = pynmea2.parse(raw_data)
                    latitude = "{:.6f}".format(msg.latitude)
                    longitude = "{:.6f}".format(msg.longitude)
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
                    return float(latitude), float(longitude)
                except pynmea2.ParseError as e:
                    print(f"Parse error: {e}")

gps_serial_port = '/dev/ttyUSB0' 
ser_gps = serial.Serial(gps_serial_port, baudrate=38400, timeout=1)
rover_serial_port = '/dev/ttyUSB1' 
ser_rover = serial.Serial(rover_serial_port, baudrate=1000000, timeout=1)

def send_movement_command(command):
    ser_rover.write((json.dumps(command) + '\n').encode('utf-8'))

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2_rad - lon1_rad
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon)
    y = math.sin(dlon) * math.cos(lat2_rad)
    initial_bearing = math.atan2(y, x)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing