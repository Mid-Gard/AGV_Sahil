import serial
import json
import time
ser = serial.Serial('/dev/ttyUSB0',baudrate=1000000, timeout=1)
def send_forward_command():
	forward_command ={"T":1,"L":255,"R":-255}
	ser.write((json.dumps(forward_command) + '\n').encode('utf-8'))

try:
	send_forward_command()
	time.sleep(20)
	
except Exception as e:
	print(f"Error:  {e}")
	
finally:
	stop_command = {"T": 0}
	ser.write((json.dumps(stop_command) + '\n').encode('utf-8'))
	ser.close()
 
			
