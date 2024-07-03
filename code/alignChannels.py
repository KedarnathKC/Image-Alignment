import numpy as np

def SSD(img1,img2):
    return np.sum((img1-img2)**2)

def CosineSimilarity(img1,img2):
    return 1-np.sum((img1*img2)/(np.linalg.norm(img1)*np.linalg.norm(img2)))

def alignChannels(img, max_shift):
    color_img = img.copy()
    distGreen = float('inf')
    distBlue = float('inf')
    colorImgGreen = np.zeros(img.shape[0:2])
    colorImgBlue = np.zeros(img.shape[0:2])
    pred_shift = np.zeros((2,2))

    for i in range(-1*max_shift[0],max_shift[0]+1):
        for j in range(-1*max_shift[1],max_shift[1]+1):
            color_img[:, :, 1] = np.roll(img[:, :, 1], [i, j], axis=[0, 1])
            color_img[:, :, 2] = np.roll(img[:, :, 2], [i, j], axis=[0, 1])
            # dist=SSD(img[:,:,0],color_img[:,:,1])
            dist=CosineSimilarity(img[:,:,0],color_img[:,:,1])
            if(distGreen>dist):
                distGreen=dist
                colorImgGreen=np.roll(img[:, :, 1], [i, j], axis=[0, 1])
                pred_shift[0]=[i,j]

            # dist=SSD(img[:,:,0],color_img[:,:,2])
            dist=CosineSimilarity(img[:,:,0],color_img[:,:,2])
            
            if(distBlue>dist):
                distBlue=dist
                colorImgBlue=np.roll(img[:, :, 2], [i, j], axis=[0, 1])
                pred_shift[1]=[i,j]
   
    color_img[:,:,1]=colorImgGreen
    color_img[:,:,2]=colorImgBlue
    
    return color_img,pred_shift

