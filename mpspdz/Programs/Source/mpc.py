from Compiler.compilerLib import Compiler
from Compiler.library import else_, if_e, print_ln, sfix, cfix, sint
from Compiler.mpc_math import pow_fx, cos, sqrt_simplified_fx
from Compiler.program import Program
import sys

compiler = Compiler()

def get_geo_distance(lat1, long1, lat2, long2):
    earth_radius = 6371
    mean_lat = (lat1 + lat2) / 2.0
    D = earth_radius * sqrt_simplified_fx(pow_fx(lat2-lat1, 2) + pow_fx(cos(mean_lat) * (long2-long1), 2))
    return D

def deg2rad(angle):
    pi = 3.14159265358
    return angle * pi/180.0

@compiler.register_function('mpc')
def mpc():
    sfix.set_precision(f=63)
    cfix.set_precision(f=63)
    VRM = sint.get_input_from(0)
    IS_DIESEL = sint.get_input_from(0)
    EU_EMISSION_STANDARD = sint.get_input_from(0)
    time_1 = sfix.get_input_from(0)
    lat_1 = deg2rad(sfix.get_input_from(0))
    long_1 = deg2rad(sfix.get_input_from(0))
    time_2 = sfix.get_input_from(0)
    lat_2 = deg2rad(sfix.get_input_from(0))
    long_2 = deg2rad(sfix.get_input_from(0))
    center_lat = deg2rad(sfix.get_input_from(1))
    center_long = deg2rad(sfix.get_input_from(1))
    radius = sfix.get_input_from(1)
    pence_per_100m = sfix.get_input_from(1)
    vehicle_radius = get_geo_distance(lat_2, long_2, center_lat, center_long)

    @if_e(((EU_EMISSION_STANDARD < 6).bit_and(IS_DIESEL == 1).bit_or(EU_EMISSION_STANDARD < 4)).reveal())
    def _():
        pence_per_100m.update(pence_per_100m * 2)
    @else_
    def _():
        pass
    distance_travelled = get_geo_distance(lat_1, long_1, lat_2, long_2)
    @if_e((vehicle_radius < radius).reveal())
    def _():
        price = distance_travelled.reveal() * 10 * pence_per_100m.reveal()
        print_ln("Price: %s", price)
        print_ln("Distance: %s", distance_travelled.reveal())
    @else_
    def _():
        print_ln("Not in radius")
        print_ln("Distance: %s", distance_travelled.reveal())



if __name__ == "__main__":
    compiler.compile_func()