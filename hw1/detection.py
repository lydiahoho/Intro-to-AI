import os
import cv2
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    with open(dataPath,'r') as f:
      content = f.read().splitlines()
    line=0
    while line<len(content):
      fline=content[line].split( )
      name=fline[0]
      people=fline[1]
      line+=1
      img=cv2.imread("data/detect/"+name)
      img_gray=cv2.imread("data/detect/"+name,0)
      for i in range (int(people)):
        loc=content[line].split( )
        x=int(loc[0])
        y=int(loc[1])
        xx=int(loc[2])
        yy=int(loc[3])
        line+=1
        face=cv2.resize(img_gray[y:y+yy,x:x+xx],(19,19),interpolation=cv2.INTER_LINEAR )
        if clf.classify(face)==1:
          cv2.rectangle(img,(x,y),(x+xx,y+yy),(0,255,0),2)
        else:
          cv2.rectangle(img,(x,y),(x+xx,y+yy),(0,0,255),2)

      cv2.imshow("result-"+name,img)
      cv2.waitKey(0)
    # End your code (Part 4)
