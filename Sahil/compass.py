import serial
import pynmea2

def get_compass_data(serial_port):
    with serial.Serial(serial_port, 38400, timeout=1) as ser:
        while True:
            raw_data = ser.readline().decode('utf-8')
            if raw_data.startswith('$'):
                try:
                    msg = pynmea2.parse(raw_data)
                    if isinstance(msg, pynmea2.VTG):
                        print("True track angle (degrees):", msg.true_track)
                    elif isinstance(msg, pynmea2.HDT):
                        print("True heading (degrees):", msg.heading)
                except pynmea2.ParseError as e:
                    print("Parse error:", e)

# Example usage
gps_serial_port = '/dev/ttyUSB0'  # Update this with your GPS serial port
get_compass_data(gps_serial_port)
