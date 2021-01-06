def ques_2a():
    M,N = 1001,1001
    u0, v0 = 100,200
    sin_img = np.zeros((M,N))
    for m in range(M):
        for n in range(N):
            term1 = 2*np.pi*m/M
            term2 = 2*np.pi*n/N
            sin_img[m,n] = np.sin(term1+term2)
        
    f = np.fft.fft2(sin_img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    
    plt.subplot(121),plt.imshow(sin_img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.show()
    
    return

def get_ideal_low_pass_filter(shape, cutoff):

    d0 = cutoff
    rows, columns = shape
    mask = np.zeros((rows, columns), dtype=np.int32)
    mid_R, mid_C = int(rows/2), int(columns/2)
    for i in range(rows):
        for j in range(columns):
            d = math.sqrt((i - mid_R)**2 + (j - mid_C)**2)
            if d <= d0:
                mask[i, j] = 1
            else:
                mask[i, j] = 0
    return mask

def get_gaussian_low_pass_filter(shape, cutoff=100):
    d0 = cutoff
    rows, columns = shape
    mask = np.zeros((rows, columns))
    mid_R, mid_C = int(rows / 2), int(columns / 2)
    for i in range(rows):
        for j in range(columns):
            d = math.sqrt((i - mid_R) ** 2 + (j - mid_C) ** 2)
            mask[i, j] = np.exp(-(d * d) / (2 * d0 * d0))
            
    return mask


def post_process(image):
    "Performs Full Contrast Stretching"
    a = 0
    b = 255
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
                

def ques_2bc(img, cutoff, filter_name='ideal_low_pass'):
    
    shape = img.shape
    if filter_name == 'ideal_low_pass':
        mask = get_ideal_low_pass_filter(shape, cutoff)
    elif filter_name == 'gaussian_low_pass':
        mask = get_gaussian_low_pass_filter(shape, cutoff)        
    else:
        print('Unknown Filter.')
        import sys
        sys.exit(1)
        
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
    mag = np.abs(ifft)
    
    filtered_image = mag#post_process(mag)
    
    return [np.uint8(filtered_image), np.uint8(dft), np.uint8(filtered_dft)]