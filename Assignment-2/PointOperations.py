def PointOperations(low_light1_path:Path, low_light2_path:Path, low_light3_path:Path, hazy_path:Path, stoneface_path:Path):
    low_light1_data = skimage.io.imread(low_light1_path.as_posix(), as_gray=True)
    low_light2_data = skimage.io.imread(low_light2_path.as_posix(), as_gray=True)
    low_light3_data = skimage.io.imread(low_light3_path.as_posix(), as_gray=True)
    hazy_data = skimage.io.imread(hazy_path.as_posix(), as_gray=True)
    stoneface_data = skimage.io.imread(stoneface_path.as_posix(), as_gray=True)
    
    low_light1_data = low_light1_data.astype('double')/255.0
    low_light2_data = low_light2_data.astype('double')/255.0
    low_light3_data = low_light3_data.astype('double')/255.0
    hazy_data = hazy_data.astype('double')/255.0
    stoneface_data = stoneface_data.astype('double')/255.0
    
    
    ''' Linear Contrast Stretching '''
    _alpha = 5
    low_light1_modified = low_light1_data * _alpha
    low_light2_modified = low_light2_data * _alpha
    low_light1_modified[low_light1_modified>1] = 1
    low_light2_modified[low_light2_modified>1] = 1
    
    plt.figure(figsize=(20,10))
    plt.subplot(221)
    plt.imshow(low_light1_data, cmap='gray')
    plt.subplot(222)
    plt.imshow(low_light1_modified, cmap='gray')
    plt.subplot(223)
    plt.imshow(low_light2_data, cmap='gray')
    plt.subplot(224)
    plt.imshow(low_light2_modified, cmap='gray')
    plt.suptitle(f'Linear Contrast Stretching\ngain = {_alpha}\n', fontsize=28)
    plt.colorbar()
    plt.show()
    
    #bins = np.arange(0,256)
    #plt.figure(figsize=(20,10))
    #plt.subplot(221)
    #plt.plot(bins, np.histogram(low_light1_data.ravel(),256,[0,256])[0])
    #plt.subplot(222)
    #plt.plot(bins, np.histogram(low_light1_modified.ravel(),256,[0,256])[0])
    #plt.subplot(223)
    #plt.plot(bins, np.histogram(low_light2_data.ravel(),256,[0,256])[0])
    #plt.subplot(224)
    #plt.plot(bins, np.histogram(low_light2_modified.ravel(),256,[0,256])[0])
    #plt.show()
    
    ''' Power Law Contrast Stretching '''
    # power law = cr^(_gamma)
    
    ## gamma=2 for foggy image
    c = 1.0
    _gamma = 0.7
    low_light1_modified = c * (low_light1_data ** _gamma)
    low_light2_modified = c * (low_light2_data ** _gamma)
    hazy_modified = c * (hazy_data ** _gamma)
    low_light1_modified[low_light1_modified>1] = 1
    low_light2_modified[low_light2_modified>1] = 1
    hazy_modified[hazy_modified>1] = 1
    
    plt.figure(figsize=(20,10))
    plt.subplot(321)
    plt.imshow(low_light1_data, cmap='gray')
    plt.subplot(322)
    plt.imshow(low_light1_modified, cmap='gray')
    plt.subplot(323)
    plt.imshow(low_light2_data, cmap='gray')
    plt.subplot(324)
    plt.imshow(low_light2_modified, cmap= 'gray')
    plt.subplot(325)
    plt.imshow(hazy_data, cmap= 'gray')
    plt.subplot(326)
    plt.imshow(hazy_modified, cmap= 'gray')    
    plt.suptitle(f'Power Law Contrast Stretching\ngain = {_gamma}\n', fontsize=28)
    plt.colorbar()
    plt.show()    
    
    ''' Histogram Equalization '''
    # computing histograms
    hist_lowlight2 = np.zeros((256,1))
    hist_lowlight3 = np.zeros((256,1))
    hist_stoneface = np.zeros((256,1))
    hist_hazy = np.zeros((256,1))
    for i in range(low_light2_data.shape[0]):
        for j in range(low_light2_data.shape[1]):
            intensity = low_light2_data[i,j] 
            hist_lowlight2[math.floor((intensity)*256)-1,0] += 1 

    for i in range(low_light3_data.shape[0]):
        for j in range(low_light3_data.shape[1]):
            intensity = low_light3_data[i,j] 
            hist_lowlight3[math.floor((intensity)*256)-1,0] += 1
            
    for i in range(stoneface_data.shape[0]):
        for j in range(stoneface_data.shape[1]):
            intensity = stoneface_data[i,j] 
            hist_stoneface[math.floor((intensity)*256)-1,0] += 1
            
    for i in range(hazy_data.shape[0]):
        for j in range(hazy_data.shape[1]):
            intensity = hazy_data[i,j] 
            hist_hazy[math.floor((intensity)*256)-1,0] += 1
    
    # computing probs
    p_lowlight2 = np.array([hist_lowlight2[i]/np.sum(hist_lowlight2) for i in range(256)])
    p_lowlight3 = np.array([hist_lowlight3[i]/np.sum(hist_lowlight3) for i in range(256)])
    p_stoneface = np.array([hist_stoneface[i]/np.sum(hist_stoneface) for i in range(256)])
    p_hazy = np.array([hist_hazy[i]/np.sum(hist_hazy) for i in range(256)])
    
    cum_p_lowlight2 = np.cumsum(p_lowlight2)
    cum_p_lowlight3 = np.cumsum(p_lowlight3)
    cum_p_stoneface = np.cumsum(p_stoneface)
    cum_p_hazy = np.cumsum(p_hazy)
    
    lowlight2_modified = np.zeros_like(low_light2_data)
    lowlight3_modified = np.zeros_like(low_light3_data)
    stoneface_modified = np.zeros_like(stoneface_data)
    hazy_modified = np.zeros_like(hazy_data)
    
    for i in range(low_light2_data.shape[0]):
        for j in range(low_light2_data.shape[1]):
            lowlight2_modified[i,j] = math.floor(255*cum_p_lowlight2[int(255*low_light2_data[i,j])]) 
            
    
    for i in range(low_light3_data.shape[0]):
        for j in range(low_light3_data.shape[1]):
            lowlight3_modified[i,j] = math.floor(255*cum_p_lowlight3[int(255*low_light3_data[i,j])]) 
            
    for i in range(stoneface_data.shape[0]):
        for j in range(stoneface_data.shape[1]):
            stoneface_modified[i,j] = math.floor(255*cum_p_stoneface[int(255*stoneface_data[i,j])]) 
            
    for i in range(hazy_data.shape[0]):
        for j in range(hazy_data.shape[1]):
            hazy_modified[i,j] = math.floor(255*cum_p_hazy[int(255*hazy_data[i,j])]) 
            
    
    plt.figure(figsize=(20,10))
    plt.subplot(221)
    plt.imshow(low_light2_data, cmap='gray')
    plt.subplot(222)
    plt.imshow(lowlight2_modified, cmap='gray')
    plt.suptitle('Histogram Equalization', fontsize=28)
    plt.show()
    
    plt.figure(figsize=(20,10))
    plt.subplot(221)    
    plt.imshow(low_light3_data, cmap='gray')
    plt.subplot(222)
    plt.imshow(lowlight3_modified, cmap='gray')    
    plt.show()
    
    plt.figure(figsize=(20,10))
    plt.subplot(221)    
    plt.imshow(stoneface_data, cmap='gray')    
    plt.subplot(222)
    plt.imshow(stoneface_modified, cmap='gray')
    plt.show()
    
    plt.figure(figsize=(20,10))    
    plt.subplot(221)
    plt.imshow(hazy_data, cmap='gray')    
    plt.subplot(222)
    plt.imshow(hazy_modified, cmap='gray')    
    plt.show()
    
    bins = np.arange(0,256)
    plt.figure(figsize=(20,10))
    plt.subplot(421)
    plt.plot(bins, np.histogram(low_light2_data.ravel()*255.0,256,[0,256])[0])
    plt.subplot(422)
    plt.plot(bins, np.histogram(lowlight2_modified.ravel()*1.0,256,[0,256])[0])
    plt.subplot(423)
    plt.plot(bins, np.histogram(low_light3_data.ravel()*255.0,256,[0,256])[0])
    plt.subplot(424)
    plt.plot(bins, np.histogram(lowlight3_modified.ravel()*1.0,256,[0,256])[0])
    plt.subplot(425)
    plt.plot(bins, np.histogram(stoneface_data.ravel()*255.0,256,[0,256])[0])
    plt.subplot(426)
    plt.plot(bins, np.histogram(stoneface_modified.ravel()*1.0,256,[0,256])[0])
    plt.subplot(427)
    plt.plot(bins, np.histogram(hazy_data.ravel()*255.0,256,[0,256])[0])
    plt.subplot(428)
    plt.plot(bins, np.histogram(hazy_modified.ravel()*1.0,256,[0,256])[0])    
    plt.show()    
    
    # CLAHE
    def _clahe(img_path, limit):
        stoneface_data = skimage.io.imread(stoneface_path.as_posix(), as_gray=True)#.astype('double')#/255.0
        _alpha = 10
        def CLAHE(img_data, thresh, overlap = 0):
            final_image = np.zeros_like(img_data).astype('double')
            winlen_x, winlen_y = round(img_data.shape[0]/(7*(1-overlap)+1)), round(img_data.shape[1]/(7*(1-overlap)+1))
        
            for i in tqdm.tqdm(range(8)):
                for j in range(8):
                    
                    row_st, col_st = round(i*winlen_x*(1-overlap)), round(j*winlen_y*(1-overlap))
                    row_end, col_end = row_st + winlen_x, col_st + winlen_y
                
                    if row_end>=img_data.shape[0]:
                        row_end = img_data.shape[0]-1
                    if col_end>=img_data.shape[1]:
                        col_end = img_data.shape[1]-1
                    
                    win = img_data[row_st:row_end, col_st:col_end]
                    
                    # Compute histogram ...
                    counts, bin_edges = np.histogram(win.ravel(), 256, [0,256])
                    
                    # Clip the histogram ...
                    thresh = 10#limit * np.max(counts)
                    
                    clipped_counts = np.minimum(counts, thresh)

                    diff = counts - clipped_counts
                    lift_val = np.sum(diff)/256.0
                    clipped_counts = clipped_counts + lift_val
                    
                    # perform Histogram Equalization ...
                    if np.sum(counts)!=0:
                        cdf = np.cumsum(clipped_counts/np.sum(counts))
                    else:
                        cdf = np.zeros(clipped_counts.shape)
                    sk = cdf
                    
                    
                    new_image = sk[win.flatten()]
                    new_image = np.reshape(255.0*new_image, [win.shape[0], win.shape[1]])
                    
                    # overlapped portions...
                    final_image[row_st:row_end,col_st:col_end][final_image[row_st:row_end,col_st:col_end]!=0] /= 2.0
                    mask = final_image[row_st:row_end,col_st:col_end]!=0
                    masked_win = new_image*mask/2.0
                    final_image[row_st:row_end,col_st:col_end] += masked_win + (1-mask)*new_image
                    
            final_image *= 1.0
            final_image[final_image>255] = 255
            return final_image
        
        plt.figure(figsize=(20,10))
        plt.suptitle('CLAHE', fontsize=28)
        plt.subplot(131)    
        plt.imshow(stoneface_data, cmap='gray')    
        plt.subplot(132)
        plt.imshow(CLAHE(stoneface_data, limit,0), cmap='gray')
        plt.title(f'CLAHE\noverlap = {0*100}%')
        plt.subplot(133)
        plt.imshow(CLAHE(stoneface_data, limit,0.25), cmap='gray')
        plt.title(f'CLAHE\noverlap = {0.25*100}%')   
        plt.show()
        return 
        
    _clahe(stoneface_path, 0.95)
    return 