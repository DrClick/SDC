import numpy as np
import cv2
from skimage.feature import hog

from color_histogram import color_hist

def color(img, channel, color_space="RGB", bins=32, bins_range=(0,256)):
    if color_space != 'RGB':
        if color_space == 'HSV':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        elif color_space == 'LUV':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
        elif color_space == 'HLS':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
        elif color_space == 'YUV':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        elif color_space == 'YCrCb':
            feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    else: feature_image = np.copy(img)

    return color_hist(feature_image, bins, bins_range)[channel][0]


def HOG(img, pixels_per_cell=(6, 6), orient=9, cells_per_block=(2, 2)):
    feature_image = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    
    features = hog(feature_image[:,:,1], orientations=orient, 
                   pixels_per_cell=pixels_per_cell, 
                   cells_per_block=cells_per_block, 
                   visualise=False, 
                   feature_vector=True)
    
    return features