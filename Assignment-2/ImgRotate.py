def imrotate(img_path:str, degree:np.float32, interpolation='nearest'):
    
    if interpolation not in ['nearest','bilinear']:
        print("Unknown Interpolation. Plese Choose either 'nearest' or 'bilinear'")
        import sys
        sys.exit(1)    
        
    import skimage.io
    import math as ma
    # check for no. of channels
    img_data = skimage.io.imread(img_path.as_posix(), as_gray=True)
    
    rads = degree * 22/(7*180)
    h, w = img_data.shape[0], img_data.shape[1]
    
    # New size of image
    newW = int(np.ceil(abs(w*np.cos(rads)) + abs(h*np.sin(rads))) + 1)
    newH = int(np.ceil(abs(w*np.sin(rads)) + abs(h*np.cos(rads))) + 1)
    
    x0, y0 = h/2, w/2
    
    def linear_interpolation(pt1, pt2, unknown):
        temp1 = pt1[1]*((pt2[0]-unknown[0])/(pt2[0]-pt1[0]))
        temp2 = pt2[1]*((unknown[0]-pt1[0])/(pt2[0]-pt1[0]))
        return temp1 + temp2
        
    
    def bilinear_interpolation(pt1, pt2, pt3, pt4, unknown):
        if pt1[0] == pt3[0]:
            return linear_interpolation((pt1[1], pt1[2]), (pt2[1], pt2[2]), (unknown[1], unknown[2]))
        if pt1[1] == pt2[1]:
            return linear_interpolation((pt1[0], pt1[2]), (pt3[0], pt3[2]), (unknown[0], unknown[2]))
            
        R1 = linear_interpolation((pt1[0], pt1[2]), (pt3[0], pt3[2]), (unknown[0], unknown[2]))
        R2 = linear_interpolation((pt2[0], pt2[2]), (pt4[0], pt4[2]), (unknown[0], unknown[2]))
        P = linear_interpolation((pt1[1], R1), (pt2[1], R2), (unknown[1], unknown[2]))
        return P    
    
    # New image initialisation
    newImg = np.zeros([newH, newW])
    
    for i in tqdm.tqdm(range(newH)):
        for j in range(newW):
            
            # shifting the origin
            x = (newH/2 - i)
            y = (j - newW/2)
            
            # calculating new x and y co-ordinates after rotating
            xx = (x*np.cos(rads) - y*np.sin(rads))
            yy = (x*np.sin(rads) + y*np.cos(rads))
        
            xx = (h/2 - xx)
            yy = (yy + w/2)            
            
            if interpolation=='bilinear':
                x, y = xx, yy
                if (x<0 or x>=h or y<0 or y>=w):
                    newImg[i][j] = 255                
                else:
                    x1, x2 = ma.floor(x), ma.ceil(x)
                    y1, y2 = ma.floor(y), ma.ceil(y)
                    
                    x1 = x1-1 if x1==h else x1
                    x2 = x2-1 if x2==h else x2
                    y1 = y1-1 if y1==w else y1
                    y2 = y2-1 if y2==w else y2
                    
                    pt1, pt2 = (x1, y1, img_data[x1, y1]), (x1, y2, img_data[x1, y2])
                    pt3, pt4 = (x2, y1, img_data[x2, y1]), (x2, y2, img_data[x2, y2])
                    unknown = (x, y, 0)
                    
                    if pt1[0] == pt3[0] and pt1[2] == pt2[2]:
                        newImg[i, j] = img_data[int(x), int(y)]
                    else:
                        newImg[i,j] = bilinear_interpolation(pt1, pt2, pt3, pt4, unknown)
                    
            elif interpolation=='nearest':
                xx, yy = int(xx), int(yy)
  
                # checking if any of the following conditions satisfy then assigning it 255
            
                if (xx<0 or xx>=h or yy<0 or yy>=w):
                    newImg[i][j] = 255
                else:
                    newImg[i][j] = img_data[xx][yy]            
                
    #plt.imshow(newImg, cmap='gray')
    return  newImg