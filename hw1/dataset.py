import os
import cv2
import glob
def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    
    dataset = []
    face=os.path.join(dataPath,'face')
    non=os.path.join(dataPath,'non-face')
    for filename in os.listdir(face):
        img = cv2.imread(os.path.join(face,filename),cv2.IMREAD_GRAYSCALE)
        if img is not None:
            dataset.append((img,1))
            
    for filename in os.listdir(non):
        img = cv2.imread(os.path.join(non,filename),cv2.IMREAD_GRAYSCALE) 
        if img is not None:
            dataset.append((img,0))
           
    
    # End your code (Part 1)
    return dataset
