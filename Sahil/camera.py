import cv2

def main():
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Unable to open camera")
        return

    try:
        # Capture frames from the camera and display them
        while True:
            ret, frame = cap.read()  # Read a frame from the camera

            if not ret:
                print("Error: Unable to capture frame")
                break

            cv2.imshow('Camera Feed', frame)  # Display the frame
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                break
    finally:
        # Release the camera and close all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
