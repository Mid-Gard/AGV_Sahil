import Jetson.GPIO as GPIO
import time
import serial
import json
import random

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

def send_stop():
    stop_command = {"T": 0}
    ser.write((json.dumps(stop_command) + '\n').encode('utf-8'))
    print("Car Stopped")
    
def send_Right():
    # Send the command
    Right_command = {"T": 1, "L": 200, "R": -200}
    ser.write((json.dumps(Right_command) + '\n').encode('utf-8'))
    time.sleep(0.5)
    print("Turning Right")
    
def send_Left():
    # Send the command
    Left_command = {"T": 1, "L": -200, "R": 200}
    ser.write((json.dumps(Left_command) + '\n').encode('utf-8'))
    time.sleep(1)
    print("Turning Left")

def measure_distance():
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if (pulse_start - start_time) > 0.1:
            return None

    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2
    return distance

try:
    while True:
        dist = measure_distance()
        if dist is not None:
            forward_command = {"T": 1, "L": 150, "R": 150}
            ser.write((json.dumps(forward_command) + '\n').encode('utf-8'))
            print("Raw values : ", dist)
            if dist < 50:
                send_stop()
                print("Distance before turning : ", dist)
                while dist is not None and dist < 80:
                    time.sleep(0.5)
                    dist = measure_distance()
                    if dist is not None:
                        # print("Inside while loop, distance: ", dist)
                        send_Left()
                        # random.choice([send_Left, send_Right])()
                        # time.sleep(0.5)
                        send_stop()
                    else:
                        print("Timeout occurred while turning")
            # print("Distance: {:.2f} cm".format(dist))
        else:
            print("Timeout occurred")
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    ser.close()
