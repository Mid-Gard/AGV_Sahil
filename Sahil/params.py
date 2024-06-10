from dronekit import connect, VehicleMode
import math
import json
vehicle = connect('/dev/ttyUSB1', wait_ready=True, baud=57600)


'''
@vehicle.on_message('GPS_RAW_INT')
def listener(self, name, message):
    print(message.lat, message.lon)


@vehicle.on_message('ATTITUDE')
def listener(self, name, message):
    a=math.degrees(message.roll)
    print(a)
    print(message.roll, message.pitch,message.yaw)

while True:
    pass 
'''
@vehicle.on_message('GPS_RAW_INT')
def gps_listener(self, name, message):
    print("Latitude:", message.lat, "Longitude:", message.lon)

@vehicle.on_message('ATTITUDE')
def attitude_listener(self, name, message):
    roll_deg = math.degrees(message.roll)
    pitch_deg = math.degrees(message.pitch)
    yaw_deg = math.degrees(message.yaw)
    print("Roll (degrees):", roll_deg, "Pitch (degrees):", pitch_deg, "Yaw (degrees):", yaw_deg)

while True:
    pass

'''import math
import json

def main():
    gps_data = None
    attitude_data = None

    @vehicle.on_message('GPS_RAW_INT')
    def gps_listener(self, name, message):
        nonlocal gps_data
        gps_data = {'latitude': message.lat, 'longitude': message.lon}

    @vehicle.on_message('ATTITUDE')
    def attitude_listener(self, name, message):
        nonlocal attitude_data
        roll_deg = math.degrees(message.roll)
        pitch_deg = math.degrees(message.pitch)
        yaw_deg = math.degrees(message.yaw)
        attitude_data = {'roll_degrees': roll_deg, 'pitch_degrees': pitch_deg, 'yaw_degrees': yaw_deg}

    try:
        while True:
            if gps_data is not None and attitude_data is not None:
                combined_data = {**gps_data, **attitude_data}  # Combine both dictionaries
                combined_json = json.dumps(combined_data)
                print(combined_json)
                # Reset the variables for the next iteration
                gps_data = None
                attitude_data = None
    except KeyboardInterrupt:
        print("Program terminated by user.")
if __name__ == "__main__":
    main()'''