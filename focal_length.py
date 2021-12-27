# -*- coding: utf-8 -*-
# @Time    : 2021/11/4 11:15 上午
# @Author  : Yushuo Wang
# @FileName: focal_length.py
# @Software: PyCharm
# @Blog    ：https://lesliewongcv.github.io/


import cv2
import numpy as np

img = cv2.imread('/Users/leslie/Downloads/EE6427/6.jpg')
a = []
b = []
i = 1
blue = (252, 186, 3 )
light_blue =(245, 233, 66)
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global i
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        a.append(x)
        b.append(y)
        cv2.circle(img, (x, y), 1, (0, 0, 255), thickness=5)
        if i == 7:
            cv2.putText(img, str(i), (x-50, y), cv2.FONT_HERSHEY_PLAIN,
                        4.0, (0, 233, 66), thickness=4)
            cv2.putText(img, '[' + xy + ']', (x- 440, y), cv2.FONT_HERSHEY_PLAIN,
                        4.0, light_blue, thickness=4)
            cv2.imshow("image", img)
            print(x, y)
            i += 1
            return
        cv2.putText(img, str(i), (x, y), cv2.FONT_HERSHEY_PLAIN,
                    4.0, (0, 233, 66), thickness=3)
        cv2.putText(img, '['+xy+']', (x+50, y), cv2.FONT_HERSHEY_PLAIN,
                    4.0, light_blue, thickness=3)
        cv2.imshow("image", img)
        print(x, y)
        i += 1


cv2.namedWindow("image")
cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
# print(on_EVENT_LBUTTONDOWN)
cv2.imshow("image", img)
cv2.waitKey(0)
print(a[0], b[0])


