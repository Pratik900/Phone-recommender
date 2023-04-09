# image blur applied for iso 100,f_stop=f/16,shutter speed = 1/100
import cv2
import math
import numpy as np
from brisque import BRISQUE
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as ssim

# Load the image
img = cv2.imread('./static/images/front.jpg')
img = cv2.resize(img,(450,600))

# Camera Parameters
shutter_speed = 1/65
iso = 50
f_stop = 4

# Calculate the factor by which to scale the image's brightness
brightness_factor = 1 / (2 ** ((iso - 100) / 100))

# Apply the brightness scaling
brightened_img = np.clip(img * brightness_factor, 0, 255).astype(np.uint8)

# Calculate the kernel size for Gaussian blur based on the aperture value
kernel_size = int((f_stop / 2) * 1)

# Calculate the amount of blur applied in pixels
blur = math.sqrt((shutter_speed/0.01) * (iso/100) * (f_stop/16))

# Ensure that the kernel size is a positive odd integer
if kernel_size % 2 == 0:
        kernel_size += 1
        kernel_size = max(kernel_size, 1)
if kernel_size<3:
        kernel_size = 3

# Apply Gaussian blur to the color image
ksize = (kernel_size, kernel_size)
sigmaX = blur
process_img = cv2.GaussianBlur(brightened_img, ksize, sigmaX)

# Compute SSIM score between the original and blurred images
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_blurred_img = cv2.cvtColor(process_img, cv2.COLOR_BGR2GRAY)
ssim_score,ssim_map = ssim(gray_img, gray_blurred_img, data_range=gray_blurred_img.max() - gray_blurred_img.min(),full=True)
ssim_score = ssim_score*100

# Image Quality 
brisque = BRISQUE()
score = brisque.score(img)
score = 100 - score
score1 = brisque.score(process_img)
score1 = 100 - score1

# Calculate the average pixel intensity of the image
I = np.mean(process_img)
# Calculate the exposure value (EV)
EV = np.log2((f_stop ** 2) / shutter_speed)
# Calculate the lux value
lux = (256 - I) * (2 ** EV) * (2 ** np.log2(iso / 100)) / shutter_speed

# Historgam
plt.hist(process_img.ravel(),256,[0,256])
plt.savefig('plot.jpg')
hist_img = cv2.imread('plot.jpg')

# Display the original and Processed images,SSIM_map and Histogram
cv2.imshow('Original Image', img)
cv2.imshow('Processed Image', process_img)
cv2.imshow('SSIM map', ssim_map)
cv2.imshow('Histogram',hist_img)

# Printing Blur applied,ssim score,lux,and brisque score
print(f"The amount of blur applied: {blur:.2f} pixels")
print(f"SSIM score: {ssim_score:.2f} %")
print(f"Image Quality of Orignal Image: {score:.2f} %")
print(f"Image Quality of Processed Image: {score1:.2f} %")
print(f"Lux: {lux:.0f}")

cv2.waitKey(0)
cv2.destroyAllWindows()

# # ISO
# import cv2
# import numpy as np
# from skimage.metrics import structural_similarity as compare_ssim

# # Load the image
# img = cv2.imread('.\\static\\images\\rear.jpg')

# img = cv2.resize(img,(450,600))
# cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Set the desired ISO value (in this case, 800)
# iso = 95

# # Calculate the factor by which to scale the image's brightness
# brightness_factor = 1 / (2 ** ((iso - 100) / 100))

# # Apply the brightness scaling
# brightened_img = np.clip(img * brightness_factor, 0, 255).astype(np.uint8)

# # Display the noisy image
# cv2.imshow('ISO Image', brightened_img)
# cv2.imshow('OG Image', img)

# gray1 = cv2.cvtColor(brightened_img, cv2.COLOR_BGR2GRAY)
# gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Calculate the SSIM score
# ssim_score, ssim_map = compare_ssim(gray1, gray2, full=True)

# # Print the SSIM score
# print('SSIM score:', ssim_score)

# # Display the SSIM map
# cv2.imshow('SSIM map', ssim_map)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#Shutter Speed Contrast
# import cv2
# import numpy as np

# # Load the input image
# img = cv2.imread('.\\static\\images\\rear.jpg')
# img = cv2.resize(img,(350,400))
# img_adjusted = cv2.convertScaleAbs(img, alpha=1.5, beta=0)

# # Split the adjusted image into separate color channels
# b, g, r = cv2.split(img_adjusted)

# # Apply the same adjustment to each color channel
# b_adjusted = cv2.convertScaleAbs(b, alpha=1.5, beta=0)
# g_adjusted = cv2.convertScaleAbs(g, alpha=1.5, beta=0)  
# r_adjusted = cv2.convertScaleAbs(r, alpha=1.5, beta=0)

# # Merge the adjusted color channels into a single color image
# img_final = cv2.merge((b_adjusted, g_adjusted, r_adjusted))

# # Display the original and adjusted images side by side
# img_concat = np.concatenate((img, img_final), axis=1)
# cv2.imshow('Original vs Adjusted', img_concat)
# cv2.waitKey(0)


# Aperture
# import cv2
# import numpy as np

# # Set the desired exposure values
# aperture = 1

# img = cv2.imread('.\\static\\images\\rear.jpg')
# img = cv2.resize(img,(350,400))
# cv2.imshow("Image",img)

# # Apply a blur to simulate the effect of wide aperture
# kernel_size = int((aperture / 2) * 15)
# blur_kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
# Aperture_img = cv2.filter2D(img, -1, blur_kernel)

# # Display the simulated image
# cv2.imshow('Aperture Image', Aperture_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
