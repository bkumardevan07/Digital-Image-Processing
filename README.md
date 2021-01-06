# Digital-Image-Processing
This Repository contains all my solution of Assignments of course E9 241:Digital Image Processing (2020).<br/>

## Assignment - 1 <br/>
1. Histogram Computation: Compute the histogram of the image coins.png. Verify your
result using the MATLAB built-in function hist. <br/>

2. Otsu’s Binarization Algorithm. <br/>

3. Separate the foreground text from the background
using binarization. <br/>

4. Design a function in matlab/python count_connected_components.m(/.py) which
counts the number of characters excluding punctuations. <br/>

5. Write a function binary_morphology.m(/.py) which performs binarization to separate the foreground text from noisy background and returns a clean binary image of the text without noise.<br/>

## Assignment - 2 <br/>
1. Point Operations : <br/>
   a. Linear Contrast Stretching.<br/>
   b. Power Law Contrast Strtching.<br/>
   c. Histogram Equalization.<br/>
   d. Contrast Limited Histogram Equalisation (CLAHE).<br/>
   
2. Saturated Contrast Stretching: In this method the histogram of each R,G,B channel is stretched to the range of 0-255. To achieve this, assign a certain percentage of brightest pixels to 255 and certain percentage of darkest pixels to 0. Then perform linear contrast stretching.<br/>

3. Resizing an Image: Write a function resize.m (or resize.py) that accepts a grayscale image, resizing factor and a string (‘nearest’ for Nearest Neighbour interpolation and ‘bilinear’ for bilinear interpolation) as input and returns the resized image.<br/>

4. Image Rotation: Write a function ImgRotate.m (or ImgRotate.py) that accepts an image,
degree of rotation (in the counter clockwise direction with respect to the x-axis) and a string (‘nearest’ for Nearest Neighbour interpolation and ‘bilinear’ for bilinear interpolation) as input and returns the rotated image.<br/>
   
## Assignment-3 <br/>
1. Spatial domain filtering:<br/>
   a. Mitigate the noise in the image noisy.tif by filtering it with a square averaging mask of sizes 5,10 and 15.<br/>
   b. Use high boost filtering to sharpen the denoised image from part a. Choose the scaling constant for the high pass component that minimizes the mean squared error between the sharpened image and the image characters.tif.<br/>

2. Filtering in frequncy domain:<br/>
   a. Generate a M×N sinusoidal image sin(2πu 0 m/M+2πv 0 n/N) for M=N=1001, u 0 =100 and v 0 =200 and compute its DFT. To visualize the DFT of an image take logarithm of the magnitude spectrum.<br/>
   b. Filter the image characters.tif in the frequency domain using an ideal low pass filter (ILPF).<br/>
	The expression for the ILPF is<br/>
		H (u, v) = {1 D (u, v) ≤ D 0<br/>
			    0 if D (u, v)>D 0 , <br/> 

3. Homomorphic Filtering: Use homomorphic filtering to enhance the contrast of the image PET_image.tif. Use the following filter to perform the high pass filtering<br/>
	 D (u, v) =(γH−γL) [1−exp (−D 2 (u, v)/2D 02 )] + γL,<br/>
		 where γ H , γ L and D 0 are the parameters that you need to adjust through experimentation.
   

