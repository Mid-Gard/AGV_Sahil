import serial
import json
import time
from geopy.distance import geodesic
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
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
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

# Function to navigate to a waypoint using Pure Pursuit
def navigate_to_waypoint(target_position):
    global current_position
    lookahead_distance = 0.1  # Adjust as needed
    max_speed = 100  # Adjust as needed

    while calculate_distance(current_position, target_position) > lookahead_distance:
        current_position = get_current_position(gps_serial_port)

        # Calculate bearing to the target
        target_bearing = calculate_bearing(current_position, target_position)

        # Calculate the point ahead of the rover on the path
        lookahead_point = (
            current_position[0] + lookahead_distance * math.cos(math.radians(target_bearing)),
            current_position[1] + lookahead_distance * math.sin(math.radians(target_bearing))
        )

        # Calculate the steering angle
        steering_angle = calculate_bearing(current_position, lookahead_point) - calculate_bearing(current_position, target_position)

        # Normalize the steering angle to be within -180 to 180 degrees
        if steering_angle > 180:
            steering_angle -= 360
        elif steering_angle < -180:
            steering_angle += 360

        # Scale the steering angle based on the max_speed
        scaled_steering_angle = max(-1, min(1, steering_angle / 180))

        # Send movement command to the rover
        send_movement_command({"T": 1, "L": int(max_speed - abs(scaled_steering_angle) * max_speed), "R": int(max_speed + abs(scaled_steering_angle) * max_speed)})

        time.sleep(1)  # Adjust as needed

    # Stop the rover
    send_movement_command({"T": 0})
    print("Reached waypoint.")

# Example waypoints (Latitude, Longitude)
waypoints = [
    (15.40898, 73.00869)  # Example: Chicago
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
