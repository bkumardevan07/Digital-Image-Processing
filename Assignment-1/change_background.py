from pathlib import Path

import numpy as np

import skimage.io
import math
from datetime import datetime
from skimage.filters import threshold_otsu
import tqdm
from collections import Counter
import cv2

def change_background(quote_image_path: Path, bg_image_path: Path) -> np.ndarray:

    quote_data = skimage.io.imread(quote_image_path.as_posix(), as_gray= True)
    background_data = skimage.io.imread(bg_image_path.as_posix(), as_gray= True)
    quote_data = quote_data.astype('double')/255
    background_data = background_data.astype('double')/255
    
    thresh = threshold_otsu(quote_data)
    binarized_quote = quote_data <= thresh
    modified_image = np.zeros_like(quote_data) # this will be our final image
    
    for i in range(quote_data.shape[0]):
        for j in range(quote_data.shape[1]):
            if quote_data[i,j]<=thresh:
                modified_image[i,j] = quote_data[i,j]
            else:
                modified_image[i,j] = background_data[i,j]
    
    modified_image = (modified_image*255).astype('uint8')    
    return modified_image
