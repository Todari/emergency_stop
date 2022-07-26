import cv2
import numpy as np
from time import time

class Face():

    FACE_REFERENCE = [234, 454, 5]
    FACE_REFERENCE_2 = [127, 356, 168]
    MOUTH_REFERENCE = [13, 14, 308, 78]

    yawn_count_array = []
    yawn_time_array = []

    yawn_time_threshold = 1.5

    def __init__(self, landmark_list):

        self.landmark_list = landmark_list
        self.horizontal_angle = 0.0
        self.vertical_angle = 0.0

        self.point1 = 0
        self.point2 = 0
        self.point3 = 0
        self.point4 = 0

        self.yawn_count = len(self.yawn_count_array)

    def face_direction(self):

        for i in range(len(self.FACE_REFERENCE)):
            globals()['ref{}'.format(i)] = self.landmark_list[self.FACE_REFERENCE[i]]

        face_reference = [(ref0[1]+ref1[1])/2, (ref0[2]+ref1[2])/2, (ref0[3] + ref1[3])/2]
        face_dir_vector = [ref2[1]-face_reference[0],ref2[2]-face_reference[1], ref2[3]-face_reference[2]]
        face_dir_vector = [face_dir_vector[0]/face_dir_vector[2], face_dir_vector[1]/face_dir_vector[2], 1]

        self.point1 = [int(ref2[1]), int(ref2[2])]
        self.point2 = [int(ref2[1]-100*face_dir_vector[0]), int(ref2[2]-100*face_dir_vector[1])]

    def face_direction2(self):

        for i in range(len(self.FACE_REFERENCE_2)):
            globals()['ref{}'.format(i)] = self.landmark_list[self.FACE_REFERENCE_2[i]]

        face_reference = [(ref0[1]+ref1[1])/2, (ref0[2]+ref1[2])/2, (ref0[3] + ref1[3])/2]
        face_dir_vector = [ref2[1]-face_reference[0],ref2[2]-face_reference[1], ref2[3]-face_reference[2]]
        face_dir_vector = [face_dir_vector[0]/face_dir_vector[2], face_dir_vector[1]/face_dir_vector[2], 1]
        self.horizontal_angle = - np.degrees(np.arctan(face_dir_vector[0]/face_dir_vector[2]))
        self.vertical_angle = np.degrees(np.arctan(face_dir_vector[1]/face_dir_vector[2]))

        self.point3 = [int(ref2[1]), int(ref2[2])]
        self.point4 = [int(ref2[1]-100*face_dir_vector[0]), int(ref2[2]-100*face_dir_vector[1])]

    def yawn_counter(self):

        for i in range(len(self.MOUTH_REFERENCE)):
            globals()['ref{}'.format(i)] = self.landmark_list[self.MOUTH_REFERENCE[i]]

        yawn_param1 = ((ref0[1]-ref1[1])**2 + (ref0[2]-ref1[2])**2)**0.5
        yawn_param2 = ((ref2[1]-ref3[1])**2 + (ref2[2]-ref3[2])**2)**0.5

        if (yawn_param1/yawn_param2 > 0.7):
            self.yawn_time_array.append(time())
        elif (yawn_param1/yawn_param2 <= 0.7):
            if (len(self.yawn_time_array)!=0):
                if (time()-self.yawn_time_array[0] > self.yawn_time_threshold):
                    self.yawn_count_array.append(0)
            self.yawn_time_array.clear()