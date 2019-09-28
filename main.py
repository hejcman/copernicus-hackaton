#!/usr/bin/env python3

import timeit
import matplotlib.pyplot as plt
import geocoder

from sentinelhub import WmsRequest, BBox, CRS


def plot_img(img):
    """
    plots the map (duh)
    """
    plt.figure()
    plt.imshow(img)
    plt.show()


def get_bounding_box(coords=[16.5965161, 49.2266208], area='medium'):
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

    return BBox(bbox=coords_wgs84, crs=CRS.WGS84)


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
        [coords[1], coords[0]], method='reverse', key='	e9WV6aVAz4HJtjwDhjZz72OhjpnAcHHk')
    print("Country: %s" % results.country)
    print("City:    %s" % results.city)


def get_location_img(bbox):
    wms_true_color_request = WmsRequest(layer='TRUE_COLOR',
                                        bbox=bbox,
                                        width=1000, height=1000,
                                        time='latest',
                                        maxcc=0,
                                        instance_id='0d1f2199-b4b9-4bad-b88b-8b2423e57b93')

    wms_true_color_img = wms_true_color_request.get_data()
    plot_img(wms_true_color_img[-1])


if __name__ == "__main__":
    START = timeit.default_timer()

    get_avg_cloud_cover(get_bounding_box())

    STOP = timeit.default_timer()
    print('Runtime: ', STOP - START)
