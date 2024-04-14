# -*- coding:utf-8 -*-
"""
作者：知行合一
日期：2018年 10月 08日 14:22
文件名：demo.py
地点：changsha
"""
import math

"""
步骤：
一：使用opencv获取视频流
二：在画面上画一个方块
三：通过mediapipe获取手指关键点坐标
四：判断手指是否在方块区域
五：然后方块跟随手指移动
"""

# 导入相关库包
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

# mediapipe相关参数
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
# 默认是两只手
hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
  # while cap.isOpened():
  #   success, image = cap.read()
  #   if not success:
  #     print("Ignoring empty camera frame.")
  #     # If loading a video, use 'break' instead of 'continue'.
  #     continue


# 获取视像头视频流
cap = cv2.VideoCapture(0)

# 获取画面的宽度和高度
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 方块的参数
square_x = 80
square_y = 80
square_width = 150
square_color = (255,255,0)
L1 = 0
L2 = 0
on_squre = False
while True:

    # 读取每一帧
    ret,frame = cap.read()
    # 处理图像
    frame = cv2.flip(frame,1) # 围绕Y轴翻转

    # mediapipe处理图像 To improve performance, optionally mark the image as not writeable to pass by reference.
    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)

    # Draw the hand annotations on the image.
    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # 判断是否有手
    if results.multi_hand_landmarks:
        # 解析双手
        for hand_landmarks in results.multi_hand_landmarks:
            # 绘制21个关键点
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
            # print(hand_landmarks)

            # 保存21个x,y坐标
            x_list = []
            y_list = []
            # 再次遍历，遍历出每个关键的点，解析所需要的手指
            for landmark in hand_landmarks.landmark:
                # 添加x,y坐标
                x_list.append(landmark.x)
                y_list.append(landmark.y)
                # print(landmark.x)
            # print(len(x_list))
            # 获取食指关键点
            index_finger_x = int(x_list[8] * width)
            index_finger_y = int(y_list[8] * height)

            # 获取中指关键点
            middle_finger_x = int(x_list[12] * width)
            middle_finger_y = int(y_list[12] * height)

            # 计算双指距离
            figer_len = math.hypot((index_finger_x-middle_finger_x),(index_finger_y-middle_finger_y))
            print(figer_len)
            # # 画一个圆形来验证指尖
            # cv2.circle(frame,(index_finger_x,index_finger_y),10,(255,0,255),-1)
            # print(index_finger_x,index_finger_y)

            # 如果距离小于给定值30，即为激活，否则取消激活
            # 判断食指指尖是不是在方块内
            if figer_len < 30:
                if (index_finger_x > square_x) and (index_finger_x < (square_x + square_width)):
                    if (index_finger_y > square_y) and (index_finger_y < (square_y + square_width)):
                        if on_squre == False:
                            print('在方块内')
                            L1 = abs(index_finger_x - square_x) #绝对值表示
                            L2 = abs(index_finger_y - square_y)
                            on_squre = True
                            square_color = (255,0,255)
                else:
                    print('不在方块内')
            else:
                # 取消激活
                on_squre = False
                square_color = (255, 255, 0)

            if on_squre:
                square_x = index_finger_x - L1
                square_y = index_finger_y - L2

    # 画一个方块
    # cv2.rectangle(frame,(square_x,square_y),(square_x+square_width,square_y+square_width),(255,255,0),-1) #bgr
    # 画一个半透明方块
    overlay = frame.copy()
    cv2.rectangle(frame, (square_x, square_y), (square_x + square_width, square_y + square_width), square_color,-1)  # bgr
    frame = cv2.addWeighted(overlay,0.5,frame,0.5,0)

    # 显示
    cv2.imshow('Vitual drag',frame)
    # 退出出条件
    if cv2.waitKey(10) & 0xFF == ord('q'): # 27为Esc键
        break

cap.release()
cv2.destroyAllWindows()

