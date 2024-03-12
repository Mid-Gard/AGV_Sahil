import serial
import time
import json

# Configure the serial connection
ser = serial.Serial('/dev/ttyTHS1', 1000000, timeout=1)

def send_command():
    # Send the command
    forward_command = {"T": 1, "L": 255, "R": 255}
    ser.write((json.dumps(forward_command) + '\n').encode('utf-8'))
    print("Test")

try:
    send_command()
    time.sleep(20)

except Exception as e:
    print(f"error:{e}")
    
        
finally:
    stop_command = {"T":0}
    ser.write((json.dumps(stop_command) + '\n').encode('utf-8'))
    ser.close()
