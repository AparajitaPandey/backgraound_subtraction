#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:59:31 2019

@author: lncl2
"""
# By using KNN the observations are as follow:
## Process is little faster
## FPS is 2 to 9 frames per second
## time taken approax 0.15 second

import numpy as np
import cv2 as cv
import imutils
import time

cap = cv.VideoCapture('rtsp://admin:admin123@192.168.1.5:554/Streaming/Channels/901')
fgbg = cv.createBackgroundSubtractorKNN(history = 100, dist2Threshold = 160.0, detectShadows = True)

(major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')
if int(major_ver)  < 3 :
    fps = cap.get(cv.cv.CV_CAP_PROP_FPS)
    print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
else :
    fps = cap.get(cv.CAP_PROP_FPS)
    print ("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))
    #fps = fps//1   

while(1):
    num_frames = fps;
    start = time.time()
    ret, frame = cap.read()
    fgmask = fgbg.apply(frame)
    text = "Unoccupied"
    
    #kernel = np.ones((5,5),np.uint8)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(3,3))
    opening = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)
    closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
    dilation = cv.dilate(closing,kernel,iterations = 1)
    end = time.time()
    
    seconds = end - start
    
    print ("Time taken : {0} seconds".format(seconds))

    # Calculate frames per second
    fps  = num_frames / seconds;
    print ("Estimated frames per second : {0}".format(fps))
    
    
    
    cnts = cv.findContours(dilation.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
     
    for c in cnts:
        cv.createBackgroundSubtractorKNN(history = 100, dist2Threshold = 160.0, detectShadows = True)
        if cv.contourArea(c) < 1000:
            
            continue
        (x, y, w, h) = cv.boundingRect(c)
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Occupied"
        
    
    cv.putText(frame, "Roocv.createBackgroundSubtractorMOG()m Status: {}".format(text), (10, 20),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)    
    a = cv.resize(dilation, ( 600, 800 ), interpolation = cv.INTER_CUBIC)
    b = cv.resize(frame, (600, 800 ), interpolation = cv.INTER_CUBIC)
    cv.imshow('Contour', b)
    cv.imshow('frame',a)
    
    if text=="Occupied":
        
        print ("Motion detected")
    else:
        print("No motion detected")
        
    k = cv.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()




## With status Occupied and Unoccupied MOG2
