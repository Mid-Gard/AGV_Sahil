import serial
import pynmea2

def read_coordinates(serial_port):
    try:
        with serial.Serial(serial_port, 38400, timeout=1) as ser:
            while True:
                try:
                    raw_data = ser.readline().decode('utf-8').strip()

                    if raw_data.startswith('$GNRMC'):
                        try:
                            msg = pynmea2.parse(raw_data)
                            latitude = msg.latitude
                            longitude = msg.longitude
                            print(f"Latitude: {latitude}, Longitude: {longitude}")
                        except pynmea2.ParseError as e:
                            print(f"Parse error: {e}")

                except UnicodeDecodeError as e:
                    print(f"UnicodeDecodeError: {e}")
                    # Handle the error, such as logging or skipping the current line

    except KeyboardInterrupt:
        print("Program interrupted. Closing serial port.")

if __name__ == "__main__":
    read_coordinates('/dev/ttyAMA2')
