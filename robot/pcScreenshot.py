#coding=utf-8
'''
Created on 2018年10月29日

@author: Pan
'''
import os
import time
import cv2
from PIL import Image, ImageGrab
import numpy as np
import datetime

#截屏
def screen():
    im = ImageGrab.grab()
    im.save("screen.jpg")
#保存剪切板图片信息

def clipboard():
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        print ("Image: size : %s, mode: %s" % (im.size, im.mode))
        im.save("grab_grabclipboard.jpg")
    elif im:
        for filename in im:
            try:
                print ("filename: %s" % filename)
                im = Image.open(filename)            
            except IOError:
                pass #ignore this file
            else:
                print ("ImageList: size : %s, mode: %s" % (im.size, im.mode))
    else:
        print ("clipboard is empty.")

#python + opencv 实现屏幕录制
def videoScreen(time = 20, filename='a.avi'):
    screen = ImageGrab.grab()#获得当前屏幕
    length,width=screen.size#获得当前屏幕的大小
    video_decode_style = cv2.VideoWriter_fourcc(*'XVID')#编码格式
    video = cv2.VideoWriter(filename, video_decode_style, 32, (length, width))#输出文件命名为a.mp4,帧率为32，可以调节
    startTime = datetime.datetime.now();
    while True:
        im = ImageGrab.grab()
        imm=cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)#转为opencv的BGR格式
        video.write(imm)
        nowTime = datetime.datetime.now();
        if (nowTime - startTime).seconds > time :
            break 
    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    videoScreen()
