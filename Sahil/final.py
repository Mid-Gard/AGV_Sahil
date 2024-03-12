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
                    latitude = "{:.4f}".format(msg.latitude)
                    longitude = "{:.4f}".format(msg.longitude)
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
                    return float(latitude), float(longitude)
                except pynmea2.ParseError as e:
                    print(f"Parse error: {e}")

gps_serial_port = '/dev/ttyAMA2' 
ser_gps = serial.Serial(gps_serial_port, baudrate=38400, timeout=1)

rover_serial_port = '/dev/ttyS0' 
ser_rover = serial.Serial(rover_serial_port, baudrate=1000000, timeout=1)

def send_movement_command(command):
    ser_rover.write((json.dumps(command) + '\n').encode('utf-8'))

def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    R = 6371e3  
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    initial_theta = math.atan2(y, x)
    initial_bearing = (math.degrees(initial_theta) + 360) % 360

    return distance, initial_bearing
def get_initial_direction():
    # Read initial GPS coordinates
    initial_position = get_current_position(gps_serial_port)
    time.sleep(5)  # Wait for a short period to observe changes

    # Read GPS coordinates again
    current_position = get_current_position(gps_serial_port)

    # Calculate initial bearing based on the change in coordinates
    _, initial_direction = calculate_bearing(initial_position[0], initial_position[1],
                                             current_position[0], current_position[1])

def navigate_to_waypoint(current_position, target_position):
    lat1, lon1 = current_position
    lat2, lon2 = target_position

    distance, bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    print(f"Distance to waypoint: {distance:.2f} meters, Bearing: {bearing:.2f}°")
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
    while distance > 1.0:  # Adjust the threshold as needed
        current_position = get_current_position(gps_serial_port)
        distance, _ = calculate_bearing(current_position[0], current_position[1], lat2, lon2)
        time.sleep(1)

    print("Waypoint reached!")

    
if __name__ == "__main__":
    waypoints = [
        (74.4111, 73.0987),  # Waypoint 1
        (15.41, 73.009),     # Waypoint 2
        (15.412, 73.01),     # Waypoint 3
        (15.415, 73.011),    # Waypoint 4
        (15.418, 73.012)     # Waypoint 5
    ]

    try:
        initial_position = get_current_position(gps_serial_port)
        print(f"Initial Position: {initial_position}")

        for waypoint in waypoints:
            navigate_to_waypoint(initial_position, waypoint)

            # Simulate reaching the waypoint (replace with actual logic)
            time.sleep(5)

            # Update the current position after reaching the waypoint
            current_position = get_current_position(gps_serial_port)
            print(f"Current Position: {current_position}")

    except KeyboardInterrupt:
        print("Program interrupted.")    
    finally:
    # Stop the rover by sending an emergency stop command
        emergency_stop_command = {"T": 0}
        send_movement_command(emergency_stop_command)

        # Close the serial connections
        ser_gps.close()
        ser_rover.close()    