import serial
def read_raw_data(serial_port):
    try:
        with serial.Serial(serial_port, 38400, timeout=1) as ser:
            print("Connected to GPS module on {}".format(serial_port))
            while True:
                raw_data = ser.readline().decode('utf-8', errors='ignore')
                print(raw_data)
    except serial.SerialException as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    read_raw_data('/dev/ttyUSB0')
