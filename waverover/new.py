import serial
import time
import json

# Configure the serial connection
ser = serial.Serial('/dev/ttyS0', 1000000, timeout=1)

def send_command(command):
    # Send the command
    forward_command = {"T": 1, "L": 175, "R": 175}
    ser.write((json.dumps(forward_command) + '\n').encode('utf-8'))
    

try:
    send_forward_command()
    time.sleep(20)

except Exception as e:
    print(f"error:{e}")
    
        
finally:
    stop_coomand = {"T":0}
    ser.write(json.dumps(stop_command) + '\n').encode('utf-8'))
    ser.close()
