import time
import Jetson.GPIO as GPIO

# Define the GPIO pin connected to the analog output of the FC-22 sensor
ANALOG_PIN = 18  # Replace 18 with the actual GPIO pin you're using

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ANALOG_PIN, GPIO.IN)

# Main loop to read sensor data
try:
    while True:
        # Read analog sensor data
        sensor_value = GPIO.input(ANALOG_PIN)
        print("Sensor Value:", sensor_value)
        
        # Optionally, convert sensor value to gas concentration using calibration data
        
        # Wait for a short duration before reading again
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()
