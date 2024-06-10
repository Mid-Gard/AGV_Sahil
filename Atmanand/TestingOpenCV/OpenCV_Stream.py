import cv2
import requests
import json
import time

# URL of your Django server endpoint to post frames to
SERVER_URL = 'http://192.168.0.186:8000/agv_rover/ir_post/'

def capture_frames_and_post():
    # Open the video capture device (change 0 to the appropriate device index if needed)
    cap = cv2.VideoCapture(0)
    # Set the resolution to 854x480 (480p)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 854)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame")
            break
        # Display the frame in a window
        cv2.imshow("Frame", frame)
        # Encode the frame as JPEG
        _, img_encoded = cv2.imencode('.jpg', frame)
        # Convert the image data to bytes
        frame_data = img_encoded.tobytes()
        try:1234
        
            # Post the frame data to the server
            response = requests.post(SERVER_URL, data=frame_data)
            print(response.text)
        except requests.exceptions.ConnectionError:
            print("Error: Connection refused. Server may be down.")
            # Sleep for a while before retrying
            time.sleep(5)
        except Exception as e:
            print("Error:", e)
            # Sleep for a while before retrying
            time.sleep(2)
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the video capture device and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_frames_and_post()
