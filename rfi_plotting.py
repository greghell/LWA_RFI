import matplotlib as mpl
import matplotlib.dates as mdates
import numpy as np, matplotlib.pyplot as plt, os, pylab, glob
import scipy.signal
from scipy.stats.stats import pearsonr
from scipy import stats
from astropy.time import Time
from slack_sdk import WebClient
import os
import requests
import time
import pycurl
from io import BytesIO
import math
import sys
from opensky_api import OpenSkyApi
from IPython import display
from datetime import datetime, timedelta, timezone
import mpu
import pytz
import csv
import requests
import cartopy.crs as ccrs
import cartopy.feature as cfeature
mpl.rcParams['timezone'] = 'US/Pacific';


def plot_air_traffic(today):
    '''
    plots map around OVRO with all airplanes in the last 24 hours, 1 minute sampling
    '''
    patAT = '/home/ghellbourg/RFItracking/flightsdata/';

    dirsAT = glob.glob(patAT+'*.npz');

    rightnow = datetime.now();

    # remove oldest files (> 25h old)
    for fil in dirsAT:
        datetime_object = datetime.strptime(fil.split('/')[-1].strip('.npz'), '%Y-%m-%d_%H:%M:%S')
        if datetime_object < rightnow - timedelta(hours=25.):
            os.remove(fil);

    fig = plt.figure(figsize=(16,12));
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree());
    ax.set_extent([-121.036,-114.482,35.238,38.665], crs=ccrs.PlateCarree());

    ax.add_feature(cfeature.LAND);
    ax.add_feature(cfeature.OCEAN);
    ax.add_feature(cfeature.COASTLINE);
    ax.add_feature(cfeature.STATES);
    ax.add_feature(cfeature.BORDERS, linestyle=':');
    ax.add_feature(cfeature.LAKES, alpha=0.5);
    ax.add_feature(cfeature.RIVERS);

    x, y = (-118.283443,37.233370);    # OVRO
    plt.scatter(x, y, s = 15, c='r');
    plt.annotate('OVRO',(x,y));
    x, y = (-118.4066103,37.3665175);  # Bishop
    plt.scatter(x, y, s = 15, c='k');
    plt.annotate('Bishop',(x,y));
    x, y = (-119.9346448,36.7857263);  # Fresno
    plt.scatter(x, y, s = 15, c='k');
    plt.annotate('Fresno',(x,y));
    x, y = (-119.1992671,35.3494663);  # Bakersfield
    plt.scatter(x, y, s = 15, c='k');
    plt.annotate('Bakersfield',(x,y));
    x, y = (-115.3150834,36.1251958);  # Las Vegas
    plt.scatter(x, y, s = 15, c='k');
    plt.annotate('Las Vegas',(x,y));

    dirsAT = glob.glob(patAT+'*.npz');
    dirsAT = np.sort(dirsAT);
    ndirsAT = len(dirsAT);

    dat = [];    #day/time
    numplanes = np.zeros((ndirsAT));    # number of planes within 30km from OVRO

    for k in range(ndirsAT):
        tmp = np.load(dirsAT[k]);
        x, y = (tmp['lon'], tmp['lat']);
        plt.scatter(x, y, s = 3, c='#EEB011', alpha=0.1+(k+1)/ndirsAT*0.9);
        dat.append(datetime.strptime(dirsAT[k].split('/')[-1].strip('.npz'), '%Y-%m-%d_%H:%M:%S').astimezone(pytz.timezone("America/Los_Angeles")));
        for kk in range(len(tmp['lon'])):
            if mpu.haversine_distance((37.233370, -118.283443), (tmp['lat'][kk], tmp['lon'][kk])) < 30.:
                numplanes[k] += 1;
    
#    today = datetime.now().strftime('%Y-%m-%d');
    plt.title(today + ' -- air traffic over OVRO');
    plt.tight_layout();
    return ax, dat, numplanes;


def air_traffic_ovro(numplanes,dat,today):
    '''
    plots with number of aircrafts within 30km of OVRO function of time
    '''
    fig, ax = plt.subplots(1,1,figsize=(16,4));
    ax.plot_date(mpl.dates.date2num(dat), numplanes,'*');
    date_format = mdates.DateFormatter('%m-%d %H:%M');
#    ax.tick_params(labelrotation=45);
    ax.xaxis.set_major_formatter(date_format);
    ax.tick_params(labelrotation=45);
    ax.grid();
    ax.set(ylabel='# of planes 30 km from OVRO',xlabel='date / time');
    plt.suptitle(today);
    plt.tight_layout();
    return ax;
