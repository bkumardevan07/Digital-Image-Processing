def SaturatedContrastStretching(img_path):
    import skimage.io
    import math as ma
    img_old = skimage.io.imread(img_path.as_posix()).astype('double')
    img_data = img_old.copy()
    
    _alpha = 5
    clip_bright = 150 # changed 50 to 200, 150 is final.
    img_data = img_data * _alpha
    img_old = img_old * _alpha
    img_data[img_data>255] = 255.0
    # channel-1
    img_data[:,:,0][img_data[:,:,0]==1] = 0.
    img_data[:,:,0][img_data[:,:,0]>200] = 255.
    
    # channel-2
    img_data[:,:,1][img_data[:,:,1]==4] = 0.
    img_data[:,:,1][img_data[:,:,1]>clip_bright] = 255.
    
    # channel-3
    img_data[:,:,2][img_data[:,:,2]==4] = 0
    img_data[:,:,2][img_data[:,:,2]>clip_bright] = 255. 

    return img_data.astype('uint8')