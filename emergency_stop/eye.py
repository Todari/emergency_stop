import cv2
import numpy as np
from time import time
from sympy import Symbol, solve

class Eye():

    LEFT_EYE_IN_REFERENCE = [145, 144, 159, 158]
    LEFT_EYE_OUT_REFERENCE = [23, 24, 27, 28, 243, 226]
    RIGHT_EYE_IN_REFERENCE = [373, 374, 385, 386]
    RIGHT_EYE_OUT_REFERENCE = [254, 253, 258, 257, 463, 446]
    EYE_CENTER_REFERENCE = [226, 446]
    IRIS_REFERENCE = [468, 473]

    eye_center_const = 4/5
    blink_count_array = []
    close_time_array = []

    """print alert threshold"""
    close_time_threshold = 2

    def __init__ (self, landmark_list):

        self.landmark_list = landmark_list
        self.blink_count = len(self.blink_count_array)
        self.left_eye_center = [0,0,0]
        self.right_eye_center = [0,0,0]

        self.point1 = 0
        self.point2 = 0
        self.point3 = 0
        self.point4 = 0

    def eye_direction(self):
        self.left_eye_center = [self.landmark_list[self.EYE_CENTER_REFERENCE[0]][1]*self.eye_center_const
        + self.landmark_list[self.EYE_CENTER_REFERENCE[1]][1]*(1-self.eye_center_const)
        , self.landmark_list[self.EYE_CENTER_REFERENCE[0]][2]*self.eye_center_const
        + self.landmark_list[self.EYE_CENTER_REFERENCE[1]][2]*(1-self.eye_center_const)
        , self.landmark_list[self.EYE_CENTER_REFERENCE[0]][3]*self.eye_center_const
        + self.landmark_list[self.EYE_CENTER_REFERENCE[1]][3]*(1-self.eye_center_const)]

        self.right_eye_center = [self.landmark_list[self.EYE_CENTER_REFERENCE[0]][1]*(1-self.eye_center_const)
        + self.landmark_list[self.EYE_CENTER_REFERENCE[1]][1]*self.eye_center_const
        , self.landmark_list[self.EYE_CENTER_REFERENCE[0]][2]*(1-self.eye_center_const)
        + self.landmark_list[self.EYE_CENTER_REFERENCE[1]][2]*self.eye_center_const
        , self.landmark_list[self.EYE_CENTER_REFERENCE[0]][3]*(1-self.eye_center_const)
        + self.landmark_list[self.EYE_CENTER_REFERENCE[1]][3]*self.eye_center_const]
        
        left_eye_vector = [self.landmark_list[self.IRIS_REFERENCE[0]][1] - self.left_eye_center[0],
        self.landmark_list[self.IRIS_REFERENCE[0]][2] - self.left_eye_center[1],
        self.landmark_list[self.IRIS_REFERENCE[0]][3] - self.left_eye_center[2]]
        left_eye_vector = [left_eye_vector[0]/left_eye_vector[2], left_eye_vector[1]/left_eye_vector[2], 1]

        right_eye_vector = [self.landmark_list[self.IRIS_REFERENCE[1]][1] - self.right_eye_center[0],
        self.landmark_list[self.IRIS_REFERENCE[1]][2] - self.right_eye_center[1],
        self.landmark_list[self.IRIS_REFERENCE[1]][3] - self.right_eye_center[2]]
        right_eye_vector = [right_eye_vector[0]/right_eye_vector[2], right_eye_vector[1]/right_eye_vector[2], 1]

        self.point1 = [int(self.landmark_list[self.IRIS_REFERENCE[0]][1])
        , int(self.landmark_list[self.IRIS_REFERENCE[0]][2])]
        self.point2 = [int(self.landmark_list[self.IRIS_REFERENCE[0]][1] - 100*left_eye_vector[0])
        , int(self.landmark_list[self.IRIS_REFERENCE[0]][2] - 100*left_eye_vector[1])]
        self.point3 = [int(self.landmark_list[self.IRIS_REFERENCE[1]][1])
        , int(self.landmark_list[self.IRIS_REFERENCE[1]][2])]
        self.point4 = [int(self.landmark_list[self.IRIS_REFERENCE[1]][1] - 100*right_eye_vector[0])
        , int(self.landmark_list[self.IRIS_REFERENCE[1]][2] - 100*right_eye_vector[1])]

    def blink_counter(self):
        
        for i in range(len(self.LEFT_EYE_IN_REFERENCE)):
            globals()['ref_li{}'.format(i)] = self.landmark_list[self.LEFT_EYE_IN_REFERENCE[i]]
        for i in range(len(self.LEFT_EYE_OUT_REFERENCE)):
            globals()['ref_lo{}'.format(i)] = self.landmark_list[self.LEFT_EYE_OUT_REFERENCE[i]]
        for i in range(len(self.RIGHT_EYE_IN_REFERENCE)):
            globals()['ref_ri{}'.format(i)] = self.landmark_list[self.RIGHT_EYE_IN_REFERENCE[i]]
        for i in range(len(self.RIGHT_EYE_OUT_REFERENCE)):
            globals()['ref_ro{}'.format(i)] = self.landmark_list[self.RIGHT_EYE_OUT_REFERENCE[i]]

        blink_param0 = ((ref_li3[1] - ref_li0[1])**2 + (ref_li3[2] - ref_li0[2])**2)**0.5 / ((ref_lo3[1] - ref_lo0[1])**2 + (ref_lo3[2] - ref_lo0[2])**2)**0.5
        blink_param1 = ((ref_li2[1] - ref_li1[1])**2 + (ref_li2[2] - ref_li1[2])**2)**0.5 / ((ref_lo2[1] - ref_lo1[1])**2 + (ref_lo2[2] - ref_lo1[2])**2)**0.5
        blink_param2 = ((ref_ri3[1] - ref_ri0[1])**2 + (ref_ri3[2] - ref_ri0[2])**2)**0.5 / ((ref_ro3[1] - ref_ro0[1])**2 + (ref_ro3[2] - ref_ro0[2])**2)**0.5
        blink_param3 = ((ref_ri2[1] - ref_ri1[1])**2 + (ref_ri2[2] - ref_ri1[2])**2)**0.5 / ((ref_ro2[1] - ref_ro1[1])**2 + (ref_ro2[2] - ref_ro1[2])**2)**0.5

        if (np.sum([blink_param0, blink_param1, blink_param2, blink_param3]) < 1.2):
            self.close_time_array.append(time())
        elif (np.sum([blink_param0, blink_param1, blink_param2, blink_param3]) >= 1.2):
            if (len(self.close_time_array)!=0):
                self.close_time_array.clear()
                self.blink_count_array.append(0)

    def is_sleeping(self):
        if (len(self.close_time_array)!=0):
            if (time()-self.close_time_array[0] > self.close_time_threshold):
                return True
            else:
                return False
        





    
            


