import serial
import json
import time
from geopy.distance import geodesic
from geopy.distance import distance as geo_distance
import pynmea2
import math

# Function to get current GPS position
def get_current_position(serial_port):
    with serial.Serial(serial_port, baudrate=38400, timeout=1) as ser_gps:
        while True:
            raw_data = ser_gps.readline().decode('utf-8', errors='ignore').strip()

            if raw_data.startswith('$GNRMC'):
                try:
                    msg = pynmea2.parse(raw_data)
                    latitude = float("{:.5f}".format(msg.latitude))
                    longitude = float("{:.5f}".format(msg.longitude))
                    return latitude, longitude
                except pynmea2.ParseError as e:
                    print(f"Parse error: {e}")

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

# Function to send movement commands to the rover
def send_movement_command(command):
    ser_rover.write((json.dumps(command) + '\n').encode('utf-8'))

# Function to navigate to a waypoint
# Function to navigate to a waypoint
# Function to navigate to a waypoint
def navigate_to_waypoint(target_position):
    global current_position  # Add this line to access the global variable
    distance_threshold = 5  # Adjust as needed
    max_distance_from_waypoint = 15  # Adjust as needed
    forward_speed = 100  # Adjust as needed

    initial_distance = geo_distance(current_position, target_position).meters

    while geo_distance(current_position, target_position).meters > distance_threshold:
        current_position = get_current_position(gps_serial_port)  # Update current position

        current_distance = geo_distance(current_position, target_position).meters
        print(f"Current distance to waypoint: {current_distance} meters")

        bearing = calculate_bearing(current_position, target_position)
        print(f"Bearing to waypoint: {bearing} degrees")

        # Set turn direction and strength
        if bearing > 0:
            send_movement_command({"T": 1, "L": forward_speed, "R": forward_speed})  # Move forward
        else:
            send_movement_command({"T": 1, "L": -forward_speed, "R": -forward_speed})  # Move backward

        time.sleep(1)

        # Check if the rover is going too far beyond the waypoint
        if current_distance > max_distance_from_waypoint + initial_distance:
            print("Rover went too far beyond the waypoint. Stopping.")
            break

    # Stop the rover
    send_movement_command({"T": 0})
    print("Reached waypoint.")
    time.sleep(2)  # Stop for 2 seconds (adjust as needed)


# Example waypoints (Latitude, Longitude)
waypoints = [
    (15.40892, 73.00882)  # Example: Chicago
]

# Configure the serial connection to the GPS module
gps_serial_port = '/dev/ttyAMA2'  # Adjust this based on your setup
ser_gps = serial.Serial(gps_serial_port, baudrate=38400, timeout=1)

# Configure the serial connection to the ESP32 (Rover)
rover_serial_port = '/dev/ttyS0'  # Adjust this based on your setup
ser_rover = serial.Serial(rover_serial_port, baudrate=1000000, timeout=1)

try:
    while True:
        current_position = get_current_position(gps_serial_port)

        for waypoint in waypoints:
            print(f"Current position: {current_position}")
            print(f"Target waypoint: {waypoint}")
            navigate_to_waypoint(waypoint)
            time.sleep(5)  # Adjust as needed

except KeyboardInterrupt:
    pass
finally:
    # Stop the rover by sending an emergency stop command
    emergency_stop_command = {"T": 0}
    send_movement_command(emergency_stop_command)

    # Close the serial connections
    ser_gps.close()
    ser_rover.close()