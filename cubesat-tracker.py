"""
Author: Jim Labilles
Email: jim@cyberops.com.au
Date: 2024-05-15
Description: This script calculates the azimuth and elevation of a satellite from TLE data.
"""

from skyfield.api import EarthSatellite, load, wgs84

# Define TLE parameters
ts = load.timescale()
line1 = '1 45727U 20037E   24135.43144721  .00005438  00000+0  47906-3 0  9996'
line2 = '2 45727  97.7757 312.0535 0010345 230.6380 129.3926 14.96842205210896'
satellite = EarthSatellite(line1, line2, 'M2 PATHFINDER', ts)
print("[+] Tracking...")
print(satellite)

# Define observer's location (Adelaide SA 5000)
observer_lat = -34.93
observer_lon = 138.60
observer_elevation = 0

# Get current time
ts = load.timescale()
t = ts.now()

# Find when cubesat rises and sets
bluffton = wgs84.latlon(+40.8939, -83.8917)
t0 = ts.utc(2014, 1, 23)
t1 = ts.utc(2014, 1, 24)
t, events = satellite.find_events(bluffton, t0, t1, altitude_degrees=30.0)
event_names = 'rise above 30�', 'culminate', 'set below 30�'
print("\n[+] Cubesat Rises and Sets")
for ti, event in zip(t, events):
    name = event_names[event]
    print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)

# Generating Cubesat Position
t = ts.now()
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
