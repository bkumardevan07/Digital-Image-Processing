def post_process(image):
    "Performs Full Contrast Stretching"
    a = 0
    b = 1
    c = np.min(image)
    d = np.max(image)
    rows, columns = np.shape(img)
    image1 = np.zeros((rows, columns), dtype= np.int32)
    
    for i in range(rows):
        for j in range(columns):
            if (d-c)==0:
                image1[i, j] = ((b - a) / 0.000001) * (image[i, j] - c) + a
            else:
                image1[i, j] = ((b - a) / (d - c)) * (image[i, j] - c) + a
    
    return np.uint8(image1)

def homomorphic_filtering(img, _gamma_h, _gamma_l, d0):
    def get_high_pass_filter(shape, _gamma_h, _gamma_l, d0):
        rows, columns = shape
        mask = np.zeros((rows, columns), dtype=np.int32)
        mid_R, mid_C = int(rows/2), int(columns/2)
        c = _gamma_h - _gamma_l
        for i in range(rows):
            for j in range(columns):
                d = math.sqrt((i - mid_R)**2 + (j - mid_C)**2)
                mask[i,j] = c * (1-np.exp(-(d * d) / (2 * d0 * d0))) + _gamma_l

        return mask  
    
    shape = img.shape
    img = np.log(img+0.01)
    mask = get_high_pass_filter(shape, _gamma_h, _gamma_l, d0)
    fft = np.fft.fft2(img)
    shift_fft = np.fft.fftshift(fft)
    mag_dft = np.log(np.abs(shift_fft))
    dft = post_process(mag_dft)
    
    filtered_img= np.multiply(mask, shift_fft)
    mag_filtered_dft = np.log(np.abs(filtered_img)+1)
    filtered_dft = post_process(mag_filtered_dft)
    
    #inverse process...
    shift_ifft = np.fft.ifftshift(filtered_img)
    
    ifft = np.fft.ifft2(shift_ifft)
    mag = np.exp(np.abs(ifft))
    
    filtered_image = mag#post_process(mag)
    
    return [np.uint8(filtered_image), np.uint8(dft), np.uint8(filtered_dft)]   
                
                
