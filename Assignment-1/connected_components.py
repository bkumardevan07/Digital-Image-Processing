from pathlib import Path

import numpy as np

import skimage.io
import math
from datetime import datetime
from skimage.filters import threshold_otsu
import tqdm
from collections import Counter
import cv2

def count_connected_components(gray_image_path: Path) -> int:

    img_data = skimage.io.imread(gray_image_path.as_posix(), as_gray= True)
    img_data = img_data.astype('double') / 255
        
    thresh = threshold_otsu(img_data)
    binarized_data = np.zeros_like(img_data)
    binarized_data[img_data>thresh] = 1
    
    R = np.ones_like(img_data) # for connected components
    comp_index = 1
    same_comp_num = dict()
    for i in range(img_data.shape[0]):
        for j in range(img_data.shape[1]):
            if i==0 and j==0:
                if binarized_data[i,j]==0:
                    comp_index += 1
                    R[i,j] = comp_index
                    
            elif i==0:
                if binarized_data[i,j-1]!=binarized_data[i,j]:
                    if binarized_data[i,j]==0: 
                        comp_index += 1
                        R[i,j] = comp_index
                else:
                    R[i,j] = R[i,j-1]
            elif j==0:
                if binarized_data[i-1,j]!=binarized_data[i,j]:
                    if binarized_data[i,j]==0:
                        comp_index += 1
                        R[i,j] = comp_index
                else:
                    R[i,j] = R[i-1,j]
            elif binarized_data[i-1,j]==binarized_data[i,j-1]:
                if binarized_data[i,j]==binarized_data[i-1,j]:
                    R[i,j] = np.min([R[i-1,j], R[i,j-1]])
                    if R[i-1,j]!=R[i,j-1]: 
                        if not same_comp_num.get(R[i-1,j]): 
                            same_comp_num[R[i-1,j]] = set([R[i,j-1]])
                        else:
                            same_comp_num[R[i-1,j]].add(R[i,j-1])
                            
                        if not same_comp_num.get(R[i,j-1]): 
                            same_comp_num[R[i,j-1]] = set([R[i-1,j]])
                        else:
                            same_comp_num[R[i,j-1]].add(R[i-1,j])                            
                            
                elif binarized_data[i,j]==0:
                    comp_index += 1
                    R[i,j] = comp_index
            elif binarized_data[i-1,j]!=binarized_data[i,j-1]:
                if binarized_data[i,j]==binarized_data[i-1,j]:
                    R[i,j] = R[i-1,j]
                else:
                    R[i,j] = R[i,j-1]
    
    # DFS to compute connected components
    def dfs(key, same_comp_num, visited, connected_components, counter):
        visited.append(key)
        connected_components[counter].append(key)
        if same_comp_num.get(key):
            for item in same_comp_num[key]:
                if item not in visited:
                    visited = dfs(item, same_comp_num, visited, connected_components, counter)
        return visited
    
    visited = list()
    connected_components = dict()
    counter = 1
    for key in sorted(same_comp_num.keys()):
        if key not in visited:
            connected_components[counter] = []
            visited = dfs(key, same_comp_num, visited, connected_components, counter)
            counter += 1
    
    for counter_val in connected_components.keys():
        min_index = min(connected_components[counter_val])
        for ele in connected_components[counter_val]:
            R[R==ele] = min_index
    
    a,_= np.unique(R, return_counts= True)
    num_characters = a.shape[0] - 1 - 3 # 1 to exclude background count, 3 for punctuations 
    
    return num_characters
