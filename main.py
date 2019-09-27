import datetime
import numpy as np
import matplotlib.pyplot as plt

from sentinelhub import *


def plot_image(image, factor=1):
    """
    Utility function for plotting RGB images.
    """
    fig = plt.subplots(nrows=1, ncols=1, figsize=(15, 7))

    if np.issubdtype(image.dtype, np.floating):
        plt.imshow(np.minimum(image * factor, 1))
    else:
        plt.imshow(image)


coords_wgs84 = [16.55, 49.23, 16.69, 49.14]

wms_true_color_request = WmsRequest(layer='TRUE_COLOR',
                                    bbox=BBox(bbox=coords_wgs84, crs=CRS.WGS84),
                                    width=960,
                                    time='latest',
                                    maxcc=0.10,
                                    instance_id='0d1f2199-b4b9-4bad-b88b-8b2423e57b93')

wms_true_color_img = wms_true_color_request.get_data()

plt.figure()
plt.imshow(wms_true_color_img[-1])
plt.show()
