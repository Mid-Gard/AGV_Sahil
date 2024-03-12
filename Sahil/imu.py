import serial
import json

# Open serial port (change port and baudrate as per your setup)
ser = serial.Serial('/dev/ttyUSB1', 1000000, timeout=1)

# Send JSON command to request IMU information
ser.write(b'{"T":71}\n')

# Read response
response = ser.readline().decode('utf-8').strip()
print(response)

# Parse JSON response
imu_data = json.loads(response)

# Extract IMU information
#heading_angle = imu_data['heading_angle']
#acceleration = imu_data['acceleration']
# Extract other relevant IMU data as needed

# Process IMU information (example)
#print("Heading Angle:", heading_angle)
#print("Acceleration:", acceleration)
print(imu_data)
# Close serial port
ser.close()

