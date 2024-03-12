import subprocess
import requests
import json

# URL of your Django server endpoint to post frames to
SERVER_URL = 'http://192.168.0.186:8000/agv_rover/ir_post/'

def capture_frames_and_post():
    # Run the libcamera-hello command and capture its output
    process = subprocess.Popen('libcamera-hello', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Loop through the output
    for line in iter(process.stdout.readline, b''):
        line = line.decode().strip()
        # Assuming the frame data is printed to stdout in JSON format
        try:
            frame_data = json.loads(line)
            # Post the frame data to the server
            response = requests.post(SERVER_URL, json=frame_data)
            print(response.text)
        except json.JSONDecodeError:
            print('Error: Unable to decode JSON:', line)

if __name__ == "__main__":
    capture_frames_and_post()