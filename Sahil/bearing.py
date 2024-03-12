import math

def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    R = 6371e3  
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  
    y = math.sin(dlon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    initial_theta = math.atan2(y, x)
    initial_bearing = (math.degrees(initial_theta) + 360) % 360
    y = math.sin(lon2 - lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)

    final_theta = math.atan2(y, x)
    final_bearing = (math.degrees(final_theta) + 360) % 360

    return distance, initial_bearing, final_bearing

# Example usage
lat1, lon1 = 15.4089, 74.0086
lat2, lon2 = 15.4123, 74.5678

distance, initial_bearing, final_bearing = calculate_bearing(lat1, lon1, lat2, lon2)

print(f"Distance between coordinates: {distance / 1000:.4f} km")
print(f"Initial bearing: {initial_bearing:.2f}°")
print(f"Final bearing: {final_bearing:.2f}°")
