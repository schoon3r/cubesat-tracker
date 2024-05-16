"""
Author: Jim Labilles
Email: jim@cyberops.com.au
Date: 2024-05-15
Description: This script calculates the azimuth and elevation of a satellite from TLE data.
"""

from skyfield.api import EarthSatellite, load, wgs84

# Define TLE parameters
ts = load.timescale()
line1 = '1 45727U 20037E   24136.43417487  .00007361  00000+0  64613-3 0  9990' # TLE Line 1
line2 = '2 45727  97.7758 313.0504 0010341 226.8310 133.2047 14.96857924211040' # TLE Line 2
satellite = EarthSatellite(line1, line2, 'M2 PATHFINDER', ts)
print("[+] Tracking Satellite:")
print(satellite)

# Define observer's location (Sydney NSW 2000)
observer_lat = -33.88
observer_lon = 151.19
observer_elevation = 0

# Get current time
ts = load.timescale()
t = ts.now()

# Find when cubesat rises and sets
bluffton = wgs84.latlon(observer_lat, observer_lon)
t0 = ts.utc(2024, 5, 14)
t1 = ts.utc(2024, 5, 15)
t, events = satellite.find_events(bluffton, t0, t1, altitude_degrees=30.0)
event_names = 'rise above 30�', 'culminate', 'set below 30�'
print("\n[+] Cubesat Rises and Sets")
for ti, event in zip(t, events):
    name = event_names[event]
    print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

# Generating Cubesat Position
t = ts.now() # Define position according to certain time
geocentric = satellite.at(t)
print("\n[+] Cubesat Position")
print(geocentric.position.km)

# Satellite Altitude, Azimuth and Distance
difference = satellite - bluffton
topocentric = difference.at(t)
print("\n[+] Cubesat Topocentric Position")
print(topocentric.position.km)

print("\n[+] Cubesat Altitude, Azimuth, and Distance")
alt, az, distance = topocentric.altaz()
if alt.degrees > 0:
    print('The ISS is above the horizon')
print('Altitude:', alt)
print('Azimuth:', az)
print('Distance: {:.1f} km'.format(distance.km))
