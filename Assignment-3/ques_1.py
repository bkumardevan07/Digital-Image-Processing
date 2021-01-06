def _get_kernel(size):
    denr = (size * size)
    return np.ones((size,size), dtype=np.float32)/denr

def _average_filter(img,size):
    import cv2
    kernel = _get_kernel(size)
    #return cv2.filter2D(img.astype('double'),-1,kernel)
    return cv2.blur(img.astype('double'), (size,size),cv2.BORDER_REFLECT)

def _high_boost_filter(denoised_img, orig_img, thresh=1.1):
    mask = orig_img - denoised_img
    return orig_img + thresh*mask