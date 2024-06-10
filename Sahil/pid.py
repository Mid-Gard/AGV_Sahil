import serial
import json
import time
import math

def get_current_position(serial_port):
    with serial.Serial(serial_port, baudrate=38400, timeout=1) as ser_gps:
        while True:
            raw_data = ser_gps.readline().decode('utf-8', errors='ignore').strip()

            if raw_data.startswith('$GNRMC'):
                try:
                    msg = pynmea2.parse(raw_data)
                    latitude = "{:.4f}".format(msg.latitude)
                    longitude = "{:.4f}".format(msg.longitude)
                    return float(latitude), float(longitude)
                except pynmea2.ParseError as e:
                    print(f"Parse error: {e}")

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

def navigate_to_waypoint(current_position, target_position):
    lat1, lon1 = current_position
    lat2, lon2 = target_position
    distance = calculate_distance(lat1, lon1, lat2, lon2)
    bearing = calculate_bearing(lat1, lon1, lat2, lon2)
    print(f"Distance to waypoint: {distance:.2f} meters, Bearing: {bearing:.2f}°")

    while distance > 1.0:  # Adjust threshold as needed
        current_position = get_current_position(gps_serial_port)
        lat1, lon1 = current_position
        distance = calculate_distance(lat1, lon1, lat2, lon2)
        bearing = calculate_bearing(lat1, lon1, lat2, lon2)
        print(f"Distance to waypoint: {distance:.2f} meters, Bearing: {bearing:.2f}°")

        # Calculate deviation angle
        deviation_angle = math.atan2(lat2 - lat1, lon2 - lon1) - math.atan2(lat2 - lat1, lon2 - lon1)

        # Calculate deviation from the path (positive if on the right side, negative if on the left side)
        deviation_distance = math.sin(deviation_angle) * distance

        # PID control for deviation compensation
        kp = 1.0  # Proportionality constant
        ki = 0.1  # Integral constant
        kd = 0.05  # Derivative constant
        base_speed = 200  # Base speed of the rover
        error = deviation_distance
        error_diff = error - previous_error
        p = kp * error
        i = ki * (error + previous_error)
        d = kd * (error - previous_error)
        compensation = p + i + d

        # Calculate PWM values for left and right wheels
        right_pwm = base_speed + compensation
        left_pwm = base_speed - compensation

        # Ensure PWM values are within limits
        max_pwm = 255
        min_pwm = 0
        right_pwm = max(min(right_pwm, max_pwm), min_pwm)
        left_pwm = max(min(left_pwm, max_pwm), min_pwm)

        # Send movement commands
        movement_command = {"T": 1, "L": left_pwm, "R": right_pwm}
        send_movement_command(movement_command)

        # Update previous error for next iteration
        previous_error = error

    print("Waypoint reached!")

if __name__ == "__main__":
    gps_serial_port = '/dev/ttyAMA2'
    ser_gps = serial.Serial(gps_serial_port, baudrate=38400, timeout=1)

    rover_serial_port = '/dev/ttyS0'
    ser_rover = serial.Serial(rover_serial_port, baudrate=1000000, timeout=1)

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
