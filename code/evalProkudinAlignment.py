# Demo code for alignment of Prokudin-Gorskii images
#
# Your code should be run after you implement alignChannels
#
# This code is part of:
#
#   CMPSCI 670: Computer Vision
#   University of Massachusetts, Amherst
#   Instructor: Grant Van Horn
#

import os
import time
import numpy as np
import matplotlib.pyplot as plt 

from alignChannels import *
from utils import *

#Path to your data directory
data_dir = os.path.join('..', 'data', 'prokudin-gorskii')

#Path to your output directory (change this to your output directory)
out_dir = os.path.join('..', 'output', 'prokudin-gorskii')
mkdir(out_dir)

#List of images
image_names = ['00125v.jpg','00153v.jpg', '00398v.jpg', '00149v.jpg', '00351v.jpg','01112v.jpg']
# image_names = ['00153v.jpg']

#Set maximum shift alignment
max_shift = np.array([15, 15])
#Display variable
display = True

#Loop over images, untile them into images, align
for imgname in image_names:

    # Read image
    imgpath = os.path.join(data_dir, imgname)
    img = imread(imgpath)

    # Images are stacked vertically. From top to bottom B, G, R channels (not RGB)
    image_height = img.shape[0] // 3
    image_width = img.shape[1]

    # Allocating memory for the image
    channels = np.zeros((image_height, image_width, 3))

    # We are loading the color channels from top to bottom
    # Note the ordering of indices
    channels[:, :, 2] = img[0:image_height, :]
    channels[:, :, 1] = img[image_height:2*image_height, :]
    channels[:, :, 0] = img[2*image_height:3*image_height, :]

    #Cropping the image to align
    h,w,_ = channels.shape
    channels1 = channels[h//8:7*h//8,w//8:7*w//8,]

    # Align the blue and red channels to the green channel.
    color_img, pred_shift = alignChannels(channels1.copy(), max_shift)
    
    # Aligning the raw images
    channels[:,:,1] = np.roll(channels[:, :, 1], [int(pred_shift[0][0]), int(pred_shift[0][1])], axis=[0, 1])
    channels[:,:,2] = np.roll(channels[:, :, 2], [int(pred_shift[1][0]), int(pred_shift[1][1])], axis=[0, 1])

    # Cropping the raw images
    channels = channels[h//11:10*h//11,w//11:10*w//11,]

    # Print the alignments
    print('{}\n\t shift: G ({}, {})  B ({}, {})'.format(
            imgname, pred_shift[0, 0], pred_shift[0, 1], pred_shift[1, 0], pred_shift[1, 1]))
    
    # Write image output
    out_imgname = '{}-aligned.png'.format(imgname[0:-4])
    out_imgpath = os.path.join(out_dir, out_imgname)
    print(out_imgpath)
    plt.imsave(out_imgpath, channels)

    # Optionally display the results
    if display:
        plt.figure()
        plt.subplot(121)
        plt.title('Input image')
        plt.imshow(img, cmap='gray')
        plt.axis('off')

        plt.subplot(122)
        plt.title('Aligned image')
        plt.imshow(channels)
        plt.axis('off')
        plt.show(block=False)
        x = input('Press any key to continue..')
 
