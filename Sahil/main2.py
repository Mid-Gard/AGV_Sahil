import serial
import json
import time
from geopy.distance import geodesic
import math
import pynmea2

# Function to get current GPS position
def get_current_position(serial_port):
    with serial.Serial(serial_port, baudrate=38400, timeout=1) as ser_gps:
        while True:
            raw_data = ser_gps.readline().decode('utf-8',errors='ignore').strip()

            if raw_data.startswith('$GNRMC'):
                try:
                    msg = pynmea2.parse(raw_data)
                    latitude = "{:.4f}".format(msg.latitude)
                    longitude = "{:.4f}".format(msg.longitude)
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
                    return float(latitude), float(longitude)
                except pynmea2.ParseError as e:
                    print(f"Parse error: {e}")

# Configure the serial connection to the GPS module
gps_serial_port = '/dev/ttyAMA2'  # Adjust this based on your setup
ser_gps = serial.Serial(gps_serial_port, baudrate=38400, timeout=1)

# Configure the serial connection to the ESP32 (Rover)
rover_serial_port = '/dev/ttyS0'  # Adjust this based on your setup
ser_rover = serial.Serial(rover_serial_port, baudrate=1000000, timeout=1)

# Function to send movement commands to the rover
def send_movement_command(command):
    ser_rover.write((json.dumps(command) + '\n').encode('utf-8'))

# Function to calculate distance between two coordinates
def calculate_distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

# Function to calculate bearing between two coordinates
def calculate_bearing(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    delta_lon = lon2 - lon1
    x = math.cos(math.radians(lat2)) * math.sin(math.radians(delta_lon))
    y = (
        math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) -
        math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(delta_lon))
    )

    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

# Function to navigate to a waypoint
def navigate_to_waypoint(current_position, target_position):
    bearing = calculate_bearing(current_position, target_position)
    print(f"Bearing to waypoint: {bearing} degrees")
    speed = 200
    if 45 < bearing <= 135:
        movement_command = {"T": 1, "L": speed, "R": -speed}  # Turn right
    elif 135 < bearing <= 225:
        movement_command = {"T": 1, "L": -speed, "R": -speed}  # Move backward
    elif 225 < bearing <= 315:
        movement_command = {"T": 1, "L": -speed, "R": speed}  # Turn left
    else:
        movement_command = {"T": 1, "L": speed, "R": speed}  # Move forward

    send_movement_command(movement_command)

# Example waypoints (Latitude, Longitude)
waypoints = [
    (15.4089, 73.0088)  # Example: Chicago
]

try:
    while True:
        current_position = get_current_position(gps_serial_port)

        for waypoint in waypoints:
            navigate_to_waypoint(current_position, waypoint)

            time.sleep(5)  # Adjust as needed

            distance = calculate_distance(current_position, waypoint)
            if distance < 1:
                break  # Move to the next waypoint

except KeyboardInterrupt:
    pass
finally:
    # Stop the rover by sending an emergency stop command
    emergency_stop_command = {"T": 0}
    send_movement_command(emergency_stop_command)

    # Close the serial connections
    ser_gps.close()
    ser_rover.close()
