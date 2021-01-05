from pathlib import Path

import numpy as np

import skimage.io
import math
from datetime import datetime
from skimage.filters import threshold_otsu
import tqdm
from collections import Counter
import cv2


def otsu_threshold(gray_image_path: Path) -> list:
    thr_w = thr_b = time_w = time_b = 0
    bin_image = None
    
    
    coins_data = skimage.io.imread(gray_image_path.as_posix(), as_gray=True)
    histg = cv2.calcHist([coins_data],[0],None,[256],[0,256]) 
    
    MN = coins_data.shape[0] * coins_data.shape[1]
    P_k = histg / MN
    k = np.reshape(np.arange(256.0), [256, 1])
    k_P_k = k * P_k
    
    # Part A
    var_w = np.zeros([256, 1])
    start = datetime.now()
    for t in range(255):
        P_C0 = np.sum(P_k[:t+1])
        P_C1 = 1 - P_C0
        mu_0 = np.sum(k_P_k[:t+1] / P_C0) if P_C0!=0 else 0
        mu_1 = np.sum(k_P_k[t+1:] / P_C1) if P_C1!=0 else 0
        var_w[t, 0] = np.sum(np.square(k[:t+1]-mu_0) * P_k[:t+1]) \
                        + np.sum(np.square(k[t+1:]-mu_1) * P_k[t+1:])
    # for t = 255
    P_C0 = np.sum(P_k)
    mu_0 = np.sum(k_P_k / P_C0)
    var_w[-1, 0] = np.sum(np.square(k-mu_0) * P_k)
    
    t_optimum_a = np.argmin(var_w)
    
    time_part_a = datetime.now() - start
    
    # Part B
    var_b = np.zeros([256,1])
    start = datetime.now()
    for t in range(255):
        W0 = np.sum(P_k[:t+1])
        W1 = 1 - W0
        mu_0 = np.sum(k_P_k[:t+1] / W0) if W0!=0 else 0
        mu_1 = np.sum(k_P_k[t+1:] / W1) if W1!=0 else 0
        mu_T = W0 * mu_0 + W1 * mu_1
        var_b[t, 0] = W0 * np.square(mu_0 - mu_T) + W1 * np.square(mu_1 - mu_T)
    
    # for t = 255
    W0 = np.sum(P_k)
    mu_0 = np.sum(k_P_k / W0)
    mu_T = W0 * mu_0
    var_b[-1, 0] = W0 * np.square(mu_0 - mu_T)
    t_optimum_b = np.argmax(var_b)
    
    time_part_b = datetime.now() - start
    
    # Binarized Image
    binarized_image_data = np.zeros([coins_data.shape[0], coins_data.shape[1]])
    binarized_image_data[coins_data>t_optimum_b] = 1
    return [t_optimum_a, t_optimum_b, time_part_a.total_seconds()*1000, time_part_b.total_seconds()*1000, binarized_image_data] # in 'msec'    

