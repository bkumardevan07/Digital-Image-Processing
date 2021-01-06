def resize(img_path, resz_fact, interpolation='nearest'):
    
    if interpolation not in ['nearest','bilinear']:
        print("Unknown Interpolation. Plese Choose either 'nearest' or 'bilinear'")
        import sys
        sys.exit(1)
        
    import skimage.io
    import math as ma
    img_data = skimage.io.imread(img_path.as_posix(), as_gray= True)
    
    h, w = img_data.shape[0], img_data.shape[1]
    
    newW, newH = int(w * float(resz_fact)), int(h * float(resz_fact))
    
    ratioW, ratioH = w/newW, h/newH
    
    newImg = np.zeros((newH, newW), np.uint8)
    
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
            
        
    
    for i in tqdm.tqdm(range(newImg.shape[0])):
        for j in range(newImg.shape[1]):
            
            if interpolation=='nearest':
            
                x, y = round(ratioH*i), round(ratioW*j)
                x = x-1 if x==h else x
                y = y-1 if y==w else y
            
                temp = img_data[x,y]
                newImg[i,j] = temp
            
            elif interpolation=='bilinear':
                
                x, y = ratioH * i, ratioW * j
                
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
            
    plt.figure(figsize=(20,10))
    plt.subplot(211)
    plt.imshow(img_data, cmap='gray')
    plt.title('original')
    plt.subplot(212)
    plt.imshow(newImg, cmap='gray')
    plt.title('new-image')
    plt.show()
                
    return newImg