import serial
import pynmea2
import sys
import webbrowser

def read_coordinates(serial_port):
    with serial.Serial(serial_port, 38400, timeout=1) as ser:
        while True:
            raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if raw_data.startswith('$GNRMC'):
                try:
                    msg = pynmea2.parse(raw_data)
                    latitude = "{:.5f}".format(msg.latitude)
                    longitude = "{:.5f}".format(msg.longitude)
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
                    map_link = f'http://maps.google.com/?q={latitude},{longitude}'
                except KeyboardInterrupt:
                    webbrowser.open(map_link)
                    sys.exit(0)
    

if __name__ == "__main__":
    read_coordinates('/dev/ttyAMA2')
