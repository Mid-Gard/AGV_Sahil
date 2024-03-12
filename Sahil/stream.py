import io
import time
import cv2
import numpy as np
import pyautogui
from flask import Flask, render_template, Response

app = Flask(_name_)

# OpenCV window name
window_name = 'Screen Display'

# Get the dimensions of the primary screen
screen_width, screen_height = pyautogui.size()

# Flask route to serve the video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

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

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=5000, debug=True)