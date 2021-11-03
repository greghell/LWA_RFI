#* * * * * /home/ghellbourg/anaconda3/bin/python3 /home/ghellbourg/RFItracking/get_flights_positions.py


import matplotlib.pyplot as plt
from opensky_api import OpenSkyApi
#from mpl_toolkits.basemap import Basemap
from IPython import display
import datetime
import numpy as np
import time

timeout = 60;   # does not run for longer than 60s

api = OpenSkyApi();
lon = [];
lat = [];
j = 0;
# bbox = (min latitude, max latitude, min longitude, max longitude)
states = None;
timeout_start = time.time();
while (states is None) and (time.time() < timeout_start + timeout):
    try:
        states = api.get_states(bbox=(35.238, 38.665, -121.036, -114.482));
    except:
        pass;

for s in states.states:
    lon.append([]);
    lon[j] = s.longitude;
    lat.append([]);
    lat[j] = s.latitude;
    j+=1;

today = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S');
np.savez('/home/ghellbourg/RFItracking/flightsdata/'+today+'.npz', lon=lon, lat=lat);
