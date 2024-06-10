import serial
import json
import time

# Open the serial port
ser = serial.Serial('/dev/ttyUSB1', 1000000, timeout=1)

try:
    # Loop to read data every 1 second
    while True:
        # Send command to request data
        ser.write(b'{"T":71}\n')

        # Read response from serial port
        response = ser.readline().decode('utf-8').strip()
        print(response)

        # Parse JSON response
        imu_data = json.loads(response)
        print(imu_data)

        # Wait for 1 second before next iteration
        time.sleep(1)

except KeyboardInterrupt:
    # Handle keyboard interrupt (Ctrl+C)
    print("Keyboard interrupt detected. Exiting...")

finally:
    # Close the serial port
    ser.close()
