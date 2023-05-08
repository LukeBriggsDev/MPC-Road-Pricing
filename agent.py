import csv
import math
import binascii
import subprocess
import re
import requests

SERVER_NAME = "http://127.0.0.1:7687"

DISTANCE = 0.1

def get_geo_distance(lat1, long1, lat2, long2):
    earth_radius = 6371
    dlong = long2 - long1
    dlat = lat2 - lat1
    a = math.pow(math.sin(dlat/2.0), 2) + math.cos(lat1) * math.cos(lat2) * math.pow(math.sin(dlong/2.0), 2)
    c = 2 * math.asin(math.sqrt(a))
    return c * earth_radius

if __name__ == "__main__":
    # Load data
    routes = ["V-M", "V-S1", "V-S2", "V-S3a", "V-S3b", "V-S3c", "V-S4", "V-Y1", "V-Y2"]
    route_dir = "IO-VNBD/Unsynchronised V and S Dataset/Uncategorised IOVNB (V and S) Dataset/V-Dataset/"
    for route in routes:
        VRM = route
        VRM_BYTES = int(binascii.hexlify(VRM.encode('utf8')), 16)
        EU_EMISSION_STANDARD = 5
        IS_DIESEL = 1
        agent_data = []
        with open(f"{route_dir}{route}.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                agent_data.append((row[" Time Since Start of Day (seconds)"], "{:.7f}".format(float(row[" Latitude (degrees)"])), "{:.7f}".format(float(row[" Longitude (degrees)"]))))
        total = 0
        first_row = agent_data[0]
        for idx, row in enumerate(agent_data[1:]):
            distance = get_geo_distance(math.radians(float(first_row[1])), math.radians(float(first_row[2])) , math.radians(float(row[1])), math.radians(float(row[2])))
            if distance > DISTANCE:
                print(f"{idx}/{len(agent_data)}")
                with open("mpspdz/Player-Data/Input-P0-0", "w") as f:
                    args = f"{VRM_BYTES} {IS_DIESEL} {EU_EMISSION_STANDARD} {' '.join(first_row)} {' '.join(row)}"
                    f.write(args)
                first_row = row
                data = {}
                r = requests.get(SERVER_NAME)
                data = r.json()
                if data["is_in_bounds"]:
                    total += float(data["price"])
                    print(data["price"])
                    print(data["distance"])
                else:
                    print("Not in Bounds")
                with open(f"data-export/{route}.csv", "a") as export:
                    try:
                        export.write(f"{row[1]},{row[2]},{float(data['price']):.2f}, {float(data['distance'])}\n")
                    except KeyError:
                        export.write(f"{row[1]},{row[2]},0.00, {float(data['distance'])}\n")
        print(total)