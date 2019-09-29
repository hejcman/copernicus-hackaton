#!/usr/bin/env python3

import timeit
import matplotlib.pyplot as plt
import geocoder
from suntime import Sun
from datetime import datetime, timedelta
import csv
import math

from sentinelhub import WmsRequest, BBox, CRS, WcsRequest

sunlight_data = [[]]
#DEFAULT_COORDS = [16.5965161, 49.2266208]
DEFAULT_COORDS = [16.648082, 49.3471944]
# 50.1664889N, 14.4714228E


def plot_img(img):
    """
    plots the map (duh)
    """
    plt.figure()
    plt.imshow(img)
    plt.show()


def write_to_csv(data):
    with open('some.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Sunrise", "Sunset", "Cloud Coverage"])
        writer.writerows(data)


def get_bounding_box(coords=DEFAULT_COORDS, area='medium'):
    """
    Calculates the top left and bottom right coordinates of the bounding box based on the center
    point supplied by the user. The only valid values for area are ('small', 'medium', 'large').
    """
    if area == 'small':
        delta = 0.02
    elif area == 'medium':
        delta = 0.05
    elif area == 'large':
        delta = 0.08
    else:
        raise ValueError(
            "Area is not of expected value ('small', 'medium', 'large')")

    coords_wgs84 = [coords[0]+delta,
                    coords[1]+delta,
                    coords[0]-delta,
                    coords[1]-delta]

    print(coords_wgs84)

    return BBox(bbox=coords_wgs84, crs=CRS.WGS84)


def get_sunlight_data(bbox, center=DEFAULT_COORDS, start_time='2016-09-28', end_time='2019-09-28'):

    sun = Sun(center[1], center[0])

    for cc in range(0, 11, 1):
        wms_true_color_request = WmsRequest(layer='TRUE_COLOR',
                                            bbox=bbox,
                                            width=1000, height=1000,
                                            time=(start_time, end_time),
                                            maxcc=cc/10,
                                            instance_id='0d1f2199-b4b9-4bad-b88b-8b2423e57b93')

        data = wms_true_color_request.get_dates()

        for date in data:
            sunrise = sun.get_sunrise_time(date)
            sunset = sun.get_sunset_time(date)

            suntime = (sunset - sunrise)
            suntime_hour = (sunset.hour - sunrise.hour)
            suntime_minute = (sunset.minute - sunrise.minute)

            sunrise_f = "%02d:%02d" % (sunrise.hour, sunrise.minute)
            sunset_f = "%02d:%02d" % (sunset.hour, sunset.minute)

            # print(sunrise_f)
            # print(sunset_f)
            suntime_number_uf = (int(suntime_hour) +
                                 round(int(suntime_minute)/60, 2))
            suntime_number_f = '{:0>5.02f}'.format(suntime_number_uf)

            #print("number: ", suntime_number_uf)
            pw = (
                (suntime_number_uf * 0.2 * 1) +
                (suntime_number_uf * 0.2 * 0.7) +
                (suntime_number_uf * 0.3 * 0.4) +
                (suntime_number_uf * 0.3 * 0.2)
            )*1000

            real_cc = cc/10
            if(real_cc < 0.31):
                kwh = pw*1
            elif(real_cc >= 0.31 and real_cc < 0.71):
                kwh = pw*0.6
            elif(real_cc >= 0.71 and real_cc < 0.91):
                kwh = pw*0.3
            elif(real_cc >= 0.91):
                kwh = pw*0.1

            sunlight_data.append([date, sunrise_f, sunset_f, "%d%%" % (
                cc*10), suntime, suntime_number_f, round(pw), round(kwh)])

    # print(sunlight_data)
    return remove_duplicates(sunlight_data)







# DONT TOUCH, IT JUST WORKS! LUKÁŚI PLS, DON'T DO IT
def remove_duplicates(L):
    uniqueList = []
    for elem in L:
        if elem == []:
            continue
        if uniqueList == []:
            uniqueList.append(elem)
        else:
            dup = False
            for i in uniqueList:
                if(elem[0] == i[0]):
                    dup = True
                    break
            if(dup == False):
                uniqueList.append(elem)
    return uniqueList


def get_avg_cloud_cover(bbox, start_time='2018-09-28', end_time='2019-09-28', verbose=True):
    """
    Finds the number of days for each cloud coverage from 0 to 100%, and returns it as a list.
    If verbose is set to True, the progress, output, and some extra info is printer to stdout.
    """

    length_prev = 0
    clouds = []

    for cc in range(0, 11, 1):
        # Setting query parameters
        wms_true_color_request = WmsRequest(layer='TRUE_COLOR',
                                            bbox=bbox,
                                            width=1000, height=1000,
                                            time=(start_time, end_time),
                                            maxcc=cc/10,
                                            instance_id='0d1f2199-b4b9-4bad-b88b-8b2423e57b93')

        # TODO: Only one satellite image per day
        if verbose:
            print("Finding %3d%% cloud coverage images..." % (cc*10))

        # Getting date data
        data = wms_true_color_request.get_dates()
        length_now = len(data)
        clouds.append(length_now-length_prev)
        length_prev = length_now

    # Get mean cloud cover
    if verbose:
        avg_cld = 0
        index = 0

        for x in range(0, len(clouds)):
            avg_cld += (index*10)*clouds[index]
            index += 1

        avg_cld /= sum(clouds)

    # Verbose output
    if verbose:
        print(clouds)
        print("Total days:                    %d" % sum(clouds))
        print("Days with <50%% cloud coverage: %d" % sum(clouds[0:4]))
        print("Average cloud cover:           %d%%" % avg_cld)

    return clouds


def print_address(coords=[16.5965161, 49.2266208]):
    results = geocoder.mapquest(
        [coords[1], coords[0]], method='reverse', key='e9WV6aVAz4HJtjwDhjZz72OhjpnAcHHk')
    print("Country: %s" % results.country)
    print("City:    %s" % results.city)


def get_days(bbox, start_time, end_time):
    wms_true_color_request = WmsRequest(layer='TRUE_COLOR',
                                        bbox=bbox,
                                        width=1500, height=1500,
                                        time=(start_time, end_time),
                                        instance_id='0d1f2199-b4b9-4bad-b88b-8b2423e57b93')
    return wms_true_color_request.get_dates()


def get_coords(address):
    results = geocoder.mapquest(
        address, key='e9WV6aVAz4HJtjwDhjZz72OhjpnAcHHk')
    print([results.lng, results.lat])
    return [results.lng, results.lat]


def get_location_img(bbox):
    wms_true_color_request = WmsRequest(layer='TRUE_COLOR',
                                        bbox=bbox,
                                        width=1000, height=1000,
                                        time='latest',
                                        maxcc=0,
                                        instance_id='0d1f2199-b4b9-4bad-b88b-8b2423e57b93')

    wms_true_color_img = wms_true_color_request.get_data()
    plot_img(wms_true_color_img[-1])


def get_cloud_data(bbox, start_time='2018-09-28', end_time='2019-09-28'):
    wms_true_color_request = WmsRequest(layer='CLOUD_LAYER',
                                        bbox=bbox,
                                        width=1000, height=1000,
                                        time=(start_time, end_time),
                                        maxcc=1,
                                        instance_id='0d1f2199-b4b9-4bad-b88b-8b2423e57b93')

    data = wms_true_color_request.get_data()
    print(data)


if __name__ == "__main__":
    START = timeit.default_timer()

    # get_avg_cloud_cover(get_bounding_box([134.48, 58.37], 'small'))
    # get_avg_cloud_cover(get_bounding_box([114.16, 38.38], 'small'))
    write_to_csv(get_sunlight_data(get_bounding_box()))
    # get_cloud_data(get_bounding_box())

    STOP = timeit.default_timer()
    print('Runtime: ', STOP - START)
