import Jetson.GPIO as GPIO
import time
import io
import serial
import json

TRIG_PIN = 38
ECHO_PIN = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

ser = serial.Serial(
    port="/dev/ttyUSB1",
    baudrate=1000000,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
    
)

def send_Stop():
    # Send the command
    Stop_command = {"T":0}
    ser.write((json.dumps(Stop_command) + '\n').encode('utf-8'))
    print("Test")

def measure_distance():
    # Set trigger to HIGH for 10 microseconds
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Wait for echo to go HIGH
    start_time = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if (pulse_start - start_time) > 0.1:
            return None

    # Record start time of pulse
    pulse_start = time.time()

    # Wait for echo to go LOW
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Record end time of pulse
    pulse_end = time.time()

    # Calculate pulse duration
    pulse_duration = pulse_end - pulse_start

    # Calculate distance (speed of sound is 34300 cm/s)
    distance = pulse_duration * 34300 / 2

    return distance

try:
    while True:
        dist = measure_distance()
        if dist is not None:
            forward_command = {"T": 1, "L": 100, "R": 100}
            ser.write((json.dumps(forward_command) + '\n').encode('utf-8'))
            print("Raw values : ", dist)
            if dist<10:
                send_Stop()
            # print("Distance: {:.2f} cm".format(dist))
        else:
            print("Timeout occurred")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    ser.close()
