#!/usr/bin/env python
# coding: utf-8

# In[38]:


def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    img_width, img_height = np.shape(img)[:2]
    background_lvl = gray[int(img_width/2)][int(img_height/100)]
    thresh_lvl = background_lvl + 60
    
    flag, thresh = cv2.threshold(blur, thresh_lvl, 255, cv2.THRESH_BINARY)
    
    return thresh


# In[20]:


import numpy as np

CARD_MAX_SIZE = 20000
CARD_MIN_SIZE = 7000
def find_cards(threshed_image):
    contours, hierarchy = cv2.findContours(threshed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key = cv2.contourArea, reverse = True)
    
    if len(contours) == 0:
        return []
    
    contours_list = []
    hier_list = []
    for i in range(len(sorted_contours)):
        contours_list.append(contours[i])
        hier_list.append(hierarchy[0][i])
        
    card_contours = []
    approx_list = []
    for i in range(len(contours_list)):
        size = cv2.contourArea(contours_list[i])
        peri = cv2.arcLength(contours_list[i], True)
        approx = np.array(cv2.approxPolyDP(contours_list[i], 0.03*peri, True), np.float32)
        
        if ((size < CARD_MAX_SIZE) and (size > CARD_MIN_SIZE)) and (len(approx) == 4) and (hier_list[i][3] == -1):
            card_contours.append(contours_list[i])
            approx_list.append(approx)
    if len(card_contours) > 0:
        return card_contours, approx_list
    else:
        return [], []


# In[7]:


import cv2
def draw_contours(image):


    thresh = preprocess(image)
    try:
        cards, approx = find_cards(thresh)
    except:
        print("card image failed to save")
        return 0

    cv2.drawContours(image, cards, -1, (0, 255, 0), 3)

    for i in range(len(cards)):
        h = np.array([[0,0],[499,0],[499,499],[0,499]],np.float32)
        transform = cv2.getPerspectiveTransform(approx[i], h)
        cards.append(cv2.warpPerspective(image, transform, (500, 500)))

#         print("Card image saved")
    


# In[4]:


get_ipython().run_line_magic('run', 'VideoStream.ipynb')
import time

WIDTH, HEIGHT = 1000, 1000
FRAMERATE = 60
def threadVideo():
        video_receiver = VideoStream().start()
        window_name = 'frame'
        while(True):
            if (cv2.waitKey(1) == ord("q")) or video_receiver.stopped:
                video_receiver.stop()
                cv2.destroyAllWindows()
                break
            frame = video_receiver.frame
            cv2.imshow(window_name, frame)
            draw_contours(frame)


# In[41]:


threadVideo()


# In[ ]:




