import io
import time
import cv2
import numpy as np
import serial
import time
from dronekit import connect, VehicleMode
import math
import json
import requests
import pyautogui
from flask import Flask, render_template, Response

ser = serial.Serial(
    port="/dev/ttyUSB1",
    baudrate=1000000,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
    
)
headersList = {
    'Accept': '/',
    'User-Agent': 'Thunder Client (https://www.thunderclient.com)',
    'Content-Type': 'application/json'
}


def send_command():
    # Send the command
    forward_command = {"T": 1, "L": 255, "R": 255}
    ser.write((json.dumps(forward_command) + '\n').encode('utf-8'))
    print("Test")

def send_Right():
    # Send the command
    Right_command = {"T": 1, "L": 255, "R": -255}
    ser.write((json.dumps(Right_command) + '\n').encode('utf-8'))
    print("Test")
    
def send_Left():
    # Send the command
    Left_command = {"T": 1, "L": 255, "R": -255}
    ser.write((json.dumps(Left_command) + '\n').encode('utf-8'))
    print("Test")

def send_Reverse():
    # Send the command
    Rev_command = {"T": 1, "L": 255, "R": -255}
    ser.write((json.dumps(Rev_command) + '\n').encode('utf-8'))
    print("Test")    

def send_Stop():
    # Send the command
    Stop_command = {"T":0}
    ser.write((json.dumps(Stop_command) + '\n').encode('utf-8'))
    print("Test")
    
def battery_info():
    try:
        ser.write(b'{"T":70}\n')
        response = ser.readline().decode('utf-8').strip()
        imu_data = json.loads(response)
        #print(imu_data)
        return imu_data
    except Exception as e:
        print("Error:", e)
        return None
      


             
app = Flask(__name__)

# OpenCV window name
screen_width, screen_height = pyautogui.size()

# Flask route to serve the video feed
@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Flask route to handle forward movement
@app.route('/forward')
def forward():
    send_command()
    
    return "Forward command received"
    
@app.route('/stop')
def stop():
    send_Stop()
    
    return "Forward command received"
# Flask route to handle backward movement
@app.route('/backward')
def backward():
    print("Moving Backward")
    send_Reverse()
    return "Backward command received"

# Flask route to handle right movement
@app.route('/right')
def right():
    print("Moving Right")
    send_Right()
    return "Right command received"

# Flask route to handle left movement
@app.route('/left')
def left():
    print("Moving Left")
    send_Left()
    return "Left command received"

@app.route('/battery')
def imu():
    a=battery_info()
    return a
 
def generate_frames():
    # Main loop to capture frames
    while True:
        # Capture the entire screen
        screen_img = pyautogui.screenshot()

        # Convert the screenshot to a format suitable for OpenCV
        frame = cv2.cvtColor(np.array(screen_img), cv2.COLOR_RGB2BGR)

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)

        # Convert the frame to bytes
        frame_bytes = buffer.tobytes()

        # Yield the frame bytes for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Flask route to render the HTML page with the video player
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    finally:
        # Close the serial connection when the application terminates
        ser.close()