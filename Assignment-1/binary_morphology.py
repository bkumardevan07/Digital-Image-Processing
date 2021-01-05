from pathlib import Path

import numpy as np

import skimage.io
import math
from datetime import datetime
from skimage.filters import threshold_otsu
import tqdm
from collections import Counter
import cv2

def binary_morphology(gray_image_path: Path) -> np.ndarray:

    noisy_data = skimage.io.imread(gray_image_path.as_posix(), as_gray= True)
    noisy_data = noisy_data.astype('double') / 255

    thresh = threshold_otsu(noisy_data)
    noisy_data[noisy_data>thresh] = 1
    noisy_data[noisy_data<=thresh] = 0

    # window construction
    def _get_row_filter(loc_i, loc_j, data):
        win_width = 3
        nparr = data[loc_i, np.max([0,loc_j-win_width//2]):1+loc_j+win_width//2]
        if loc_j<win_width//2:
            nparr = np.pad(nparr,(win_width//2 - loc_j,0),'edge')
        elif loc_j+win_width//2>data.shape[1]-1:
            nparr = np.pad(nparr,(0,loc_j+win_width//2-data.shape[1]+1),'edge')
        return nparr

    def _get_col_filter(loc_i, loc_j, data):
        win_height= 4
        nparr = data[np.max([0,loc_i-win_height//2]):1+loc_i+win_height//2, loc_j]
        if loc_i<win_height//2:
            nparr = np.pad(nparr,(win_height//2 - loc_i,0), 'edge')
        elif loc_i+win_height//2>data.shape[0]-1:
            nparr = np.pad(nparr,(0,loc_i+win_height//2 - data.shape[0]+1),'edge')
        return nparr

    def _get_row_col_filter(loc_i, loc_j, data):
        nparr_row = _get_row_filter(loc_i, loc_j, data)
        nparr_col = _get_col_filter(loc_i, loc_j, data)
        return nparr_row, nparr_col


    def _apply_dilation_win(loc_i, loc_j, data, filter_type):

        if filter_type=='row':
            nparr = _get_row_filter(loc_i,loc_j,data)
        elif filter_type=='col':
            nparr = _get_col_filter(loc_i,loc_j,data)
        dilated_val = np.max(nparr)
        return dilated_val

    def _apply_erosion_win(loc_i, loc_j, data, filter_type):

        if filter_type=='row':
            nparr = _get_row_filter(loc_i,loc_j,data)
        elif filter_type=='col':
            nparr = _get_col_filter(loc_i,loc_j,data)
        eroded_val = np.min(nparr)
        return eroded_val

    def _apply_majority_win(loc_i, loc_j, data, filter_type):

        if filter_type=='row':
            nparr = _get_row_filter(loc_i,loc_j,data)
        elif filter_type=='col':
            nparr = _get_col_filter(loc_i,loc_j,data)
        elif filter_type=='row_n_col':
            nparr_row, nparr_col = _get_row_col_filter(loc_i, loc_j, data)
            nparr = np.concatenate([nparr_row.flatten(), nparr_col.flatten()])
        mode = Counter(nparr.flatten()).most_common(1)
        return mode[0][0]

    for i in tqdm.tqdm(range(noisy_data.shape[0])):
        for j in range(noisy_data.shape[1]):
            noisy_data[i,j] = _apply_majority_win(i,j,noisy_data,filter_type='row_n_col')
    cleaned_data = noisy_data * 255

    return cleaned_data
