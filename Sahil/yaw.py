import serial
import json
import time
import math

# Open the serial port
ser = serial.Serial('/dev/ttyUSB1', 1000000, timeout=1)

try:
    # Loop to read data every 1 second
    while True:
        # Send command to request data
        ser.write(b'{"T":71}\n')

        # Read response from serial port
        response = ser.readline().decode('utf-8').strip()

        # Parse JSON response
        imu_data = json.loads(response)

        # Extract yaw value
        yaw = imu_data.get('yaw')
        if yaw is not None:
            # Convert yaw from radians to compass degrees
            yaw_degrees = (450 - (yaw * 180 / math.pi)) % 360

            print("Yaw (radians):", yaw)
            print("Yaw (compass degrees):", yaw_degrees)

        # Wait for 1 second before next iteration
        time.sleep(1)

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    print("Keyboard interrupt detected. Exiting...")

finally:
    # Close the serial port
    ser.close()
