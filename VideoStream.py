#!/usr/bin/env python
# coding: utf-8

# In[2]:


from threading import Thread
import cv2
import ctypes

class VideoStream:
    def __init__(self, resolution = (640, 480)):
        self.resolution = resolution
        self.capture = cv2.VideoCapture(0)
        self.capture.set(3, self.resolution[0])
        self.capture.set(4, self.resolution[1])
        
        
        (self.grabbed, self.frame) = self.capture.read()
        
        self.stopped = False
        
    def start(self):
        Thread(target = self.update, args = ()).start()
        return self
    
    def update(self):
        while not self.stopped: 
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.capture.read()
    
    def read(self):
        return self.frame
    
    def stop(self):
        self.stopped = True


# In[ ]:





# In[ ]:





# In[ ]:




