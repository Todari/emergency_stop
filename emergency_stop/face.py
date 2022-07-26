import cv2
import numpy as np
from time import time

class Face():

    FACE_REFERENCE = [234, 454, 5]
    MOUTH_REFERENCE = [13, 14, 308, 78]

    yawn_count_array = []
    yawn_time_array = []

    def __init__(self, landmark_list):

        self.landmark_list = landmark_list

        self.face_reference = []
        self.face_fir_vector = []
        self.horizontal_angle = 0.0
        self.vertical_angle = 0.0

        self.point1 = 0
        self.point2 = 0

        self.yawn_count = len(self.yawn_count_array)

    def face_direction(self):

        ref0 = self.landmark_list[self.FACE_REFERENCE[0]]
        ref1 = self.landmark_list[self.FACE_REFERENCE[1]]
        ref2 = self.landmark_list[self.FACE_REFERENCE[2]]

        self.face_reference = [(ref0[1]+ref1[1])/2, (ref0[2]+ref1[2])/2, (ref0[3] + ref1[3])/2]
        face_dir_vector = [ref2[1]-self.face_reference[0],ref2[2]-self.face_reference[1], ref2[3]-self.face_reference[2]]
        self.face_dir_vector = [face_dir_vector[0]/face_dir_vector[2], face_dir_vector[1]/face_dir_vector[2], 1]
        self.horizontal_angle = - np.degrees(np.arctan(self.face_dir_vector[0]/self.face_dir_vector[2]))
        self.vertical_angle = np.degrees(np.arctan(self.face_dir_vector[1]/self.face_dir_vector[2]))

        self.point1 = [int(ref2[1]), int(ref2[2])]
        self.point2 = [int(ref2[1]-100*self.face_dir_vector[0]), int(ref2[2]-100*self.face_dir_vector[1])]

    def yawn_counter(self):

        ref0 = self.landmark_list[self.MOUTH_REFERENCE[0]]
        ref1 = self.landmark_list[self.MOUTH_REFERENCE[1]]
        ref2 = self.landmark_list[self.MOUTH_REFERENCE[2]]
        ref3 = self.landmark_list[self.MOUTH_REFERENCE[3]]

        yawn_param1 = ((ref0[1]-ref1[1])**2 + (ref0[2]-ref1[2])**2)**0.5
        yawn_param2 = ((ref2[1]-ref3[1])**2 + (ref2[2]-ref3[2])**2)**0.5

        if (yawn_param1/yawn_param2 > 0.7):
            self.yawn_time_array.append(time())
        elif (yawn_param1/yawn_param2 <= 0.7):
            if (len(self.yawn_time_array)!=0):
                if (time()-self.yawn_time_array[0] > 1.5):
                    self.yawn_count_array.append(0)
            self.yawn_time_array.clear()
        