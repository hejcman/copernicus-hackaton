#!/usr/bin/env python3

import timeit
import matplotlib.pyplot as plt
import geocoder

from sentinelhub import *


def plot_img(img):
    """
    plots the map (duh)
    """
    plt.figure()
    plt.imshow(img)
    plt.show()

start = timeit.default_timer()

house_coords = [16.5965161, 49.2266208]
coords_wgs84 = [house_coords[0]+0.05,
                house_coords[1]+0.05,
                house_coords[0]-0.05,
                house_coords[1]-0.05]

wms_true_color_request = WmsRequest(layer='TRUE_COLOR',
                                    bbox=BBox(bbox=coords_wgs84, crs=CRS.WGS84),
                                    width=1000, height=1000,
                                    time='latest',
                                    maxcc=0,
                                    instance_id='0d1f2199-b4b9-4bad-b88b-8b2423e57b93')

wms_true_color_img = wms_true_color_request.get_data()

clouds = []

length_prev = 0

for x in range(0, 10, 1):
    wms_true_color_request = WmsRequest(layer='TRUE_COLOR',
                                        bbox=BBox(bbox=coords_wgs84, crs=CRS.WGS84),
                                        width=1000, height=1000,
                                        time=('2018-09-28', '2019-09-28'),
                                        maxcc=x/10,
                                        instance_id='0d1f2199-b4b9-4bad-b88b-8b2423e57b93')

    # TODO: Only one satellite image per day
    print("Finding %2d%% cloud coverage  images..." % (x*10))
    data = wms_true_color_request.get_dates()
    length_now = len(data)
    # print(data)
    clouds.append(length_now-length_prev)
    length_prev = length_now

print("\n")

results = geocoder.mapquest([house_coords[1], house_coords[0]], method='reverse', key='	e9WV6aVAz4HJtjwDhjZz72OhjpnAcHHk')
print(results.country)
print(results.city)
print(results.street)

# print(results)
print(clouds)
print("Total days: %d" % sum(clouds))
print("Days with <50%% cloud coverage: %d" % sum(clouds[0:4]))

stop = timeit.default_timer()
print('Time: ', stop - start)  

plot_img(wms_true_color_img[-1])
