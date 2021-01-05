from pathlib import Path

import numpy as np

import skimage.io
import math
from datetime import datetime
from skimage.filters import threshold_otsu
import tqdm
from collections import Counter
import cv2

def compute_hist(image_path: Path, num_bins: int) -> list:
    
    coins_data = skimage.io.imread(image_path.as_posix(), as_gray= True)
     
    # Custom function
    counts_custom = np.zeros((num_bins,1))
    base_val = 256/num_bins
    for i in range(coins_data.shape[0]):
        for j in range(coins_data.shape[1]):
            intensity = coins_data[i,j] 
            counts_custom[math.floor((intensity)*num_bins/256),0] += 1
    
    # Lib function
    counts_lib, bin_edges = np.histogram(coins_data.ravel(), num_bins, [0,256])
    bin_centre_lib = (bin_edges[:-1] + bin_edges[1:]) / 2
    bin_centre_custom = bin_centre_lib

    return [bin_centre_custom, counts_custom, bin_centre_lib, np.reshape(counts_lib,(-1,1))]    
