# Evaluation code for color image alignment.
#
# Your goal is to implement the alignChannels() function. A correct 
# implementation should have 'gt shift' + 'pred shift' = O, i.e.,
# the all zeros vector.
#
# Credits: The homework is adapted from a similar one developed by Alyosha
# Efors (UC Berkeley, previously at CMU).
#
#
# This code is part of:
#
#   COMPSCI 670: Computer Vision
#   University of Massachusetts, Amherst
#   Instructor: Grant Van Horn
#
#   Homework 1

import os
import time
import numpy as np
import matplotlib.pyplot as plt 

from randomlyShiftChannels import *
from alignChannels import *
from utils import *

#Path to your data directory
data_dir = os.path.join('..', 'data', 'sample-images')

#List of images
image_names = ['balloon.jpeg','cat.jpg', 'ip.jpg',
            'puppy.jpg', 'squirrel.jpg', 'pencils.jpg',
            'house.png', 'light.png', 'sails.png', 'tree.jpeg'];

#Maximum shift between channels
max_shift = np.array([15, 15])

#Display results or not
display = True

print(os.path.dirname(os.path.realpath(__file__)))

#Loop over images and compute alignment
print('Evaluating alignment...')
for imgname in image_names:
    # Read image
    imgpath = os.path.join(data_dir, imgname)
    img = imread(imgpath)

    # Randomly shift channels
    channels, gt_shift = randomlyShiftChannels(img.copy(), max_shift)
    # Compute alignment
    color_img, pred_shift = alignChannels(channels.copy(), max_shift)

    # Print results
    print('{}\n\t gt shift: ({}, {}) ({}, {})\n\t pred shift: ({}, {}) ({}, {})'.format(
            imgname, gt_shift[0, 0], gt_shift[0, 1], gt_shift[1, 0], gt_shift[1, 1],
            pred_shift[0, 0], pred_shift[0, 1], pred_shift[1, 0], pred_shift[1, 1]))

    # Display the results
    if display and color_img is not None:
        plt.figure()
        plt.subplot(121)
        plt.title('Input image')
        plt.imshow(channels)
        plt.axis('off')

        plt.subplot(122)
        plt.title('Aligned image')
        plt.imshow(color_img)
        plt.axis('off')
        plt.show(block=False)
        x = input('Press any key to continue...')
