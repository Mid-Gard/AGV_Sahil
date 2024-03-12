import time
import picamera
import pygame
from pygame.locals import *

def main():
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30

        # Camera warm-up time
        time.sleep(2)

        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Camera Feed")

        try:
            # Create a Pygame surface for the camera's output
            camera_output = pygame.Surface((640, 480))

            while True:
                # Capture a frame and display it
                camera.capture(camera_output, format='rgb', use_video_port=True)
                pygame.surfarray.blit_array(screen, camera_output)
                pygame.display.flip()

                # Handle events to exit the window
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return

        except KeyboardInterrupt:
            print("Stopping the camera capture.")

        finally:
            pygame.quit()

if __name__ == "__main__":
    main()
