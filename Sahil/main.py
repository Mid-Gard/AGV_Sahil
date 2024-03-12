import serial
import pynmea2

def read_coordinates(serial_port):
    with serial.Serial(serial_port, 38400, timeout=1) as ser:
        while True:
            raw_data = ser.readline().decode('utf-8').strip()
            
            if raw_data.startswith('$GNRMC'):
                try:
                    msg = pynmea2.parse(raw_data)
                    latitude = "{:.6f}".format(msg.latitude)
                    longitude = "{:.6f}".format(msg.longitude)
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
                except pynmea2.ParseError as e:
                    print(f"Parse error: {e}")

if __name__ == "__main__":
    read_coordinates('/dev/ttyAMA2')
