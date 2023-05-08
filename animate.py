from matplotlib import pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import math
from pyproj import Proj, Transformer

routes = ["V-M", "V-S1", "V-S2", "V-S3a", "V-S3b", "V-S3c", "V-S4", "V-Y1", "V-Y2"]
data = []

TRAN_4326_TO_3857 = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
  

def merc(lat, lon):
    new_lat, new_lon = TRAN_4326_TO_3857.transform(lat, lon)
    return new_lat, new_lon

RADIUS_IN_M = 2000
ZOOM = 5
ZONE_CENTER = merc(-1.512009, 52.408124)
print(ZONE_CENTER)

for route in routes:
    new_route = []
    with open(f"data-export/{route}.csv", "r") as f:
        new_route = f.readlines()
    for idx, line in enumerate(new_route):
        new_route[idx] = [float(x) for x in line.strip("\n").split(",")]

    lat_list = [x[0] for x in new_route]
    long_list = [x[1] for x in new_route]
    price_list = [x[2] for x in new_route]
    data.append((long_list, lat_list, price_list))

min_lat = ZONE_CENTER[1] - RADIUS_IN_M * ZOOM
min_long = ZONE_CENTER[0] - RADIUS_IN_M * ZOOM
max_lat = ZONE_CENTER[1] + RADIUS_IN_M * ZOOM
max_long = ZONE_CENTER[0] + RADIUS_IN_M * ZOOM

print(min_lat, min_long, max_lat, max_long)
fig = plt.figure()

ax = plt.axes(ylim=(min_lat, max_lat), 
                xlim=(min_long, max_long))
ax.set_aspect('equal', adjustable='box')

line, = ax.plot([], [], lw=2)
zone = plt.Circle(ZONE_CENTER, RADIUS_IN_M, color='pink', alpha=0.5)

plt.ylabel("Latitude")
plt.xlabel("Longitude")
plt.rcParams.update({'font.size': 12})

plotlays, plotcols = [9], ["black","red", "yellow", "blue", "green", "magenta", "orange", "cyan", "sienna"]
lines = []
for i in range(len(routes)):
    lobj = ax.plot([], [], lw=1, color=plotcols[i], alpha=0.75, label=routes[i])[0]
    lines.append(lobj)
ax.add_artist(zone)
ax.legend()

def init():
    for idx, line in enumerate(lines):
        lines[idx].set_data([],[])
    return lines,

line_coords = []
for i in range(len(lines)):
    line_coords.append(([], []))


def animate(i):
    for n in range(len(lines)):
        try:
            x = data[n][0][i]
            y = data[n][1][i]
            price = sum(data[n][2][:i])
        except IndexError:
            x = data[n][0][-1]
            y = data[n][1][-1]
            price = sum(data[n][2][:i])
        x, y = merc(x, y)
        print(x, y)
        line_coords[n][0].append(x)
        line_coords[n][1].append(y)
        x_list = [line_coords[x][0] for x in range(len(line_coords))]
        y_list = [line_coords[y][1] for y in range(len(line_coords))]
        lines[n].set_label(routes[n] + f" {float(price):.2f}")
        ax.legend(loc=1, prop={'size': 6})
        lines[n].set_data(x_list[n], y_list[n])
    return lines + [zone]

anim = FuncAnimation(fig, animate, init_func=init, frames=max([len(data[x][0]) for x in range(len(lines))]), interval=1)
anim.save("journey2.mp4", writer="ffmpeg", fps=30, dpi=300)
fig.savefig("final.svg")

