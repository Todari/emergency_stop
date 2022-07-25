import cv2
import mediapipe as mp
import numpy as np
from time import time

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

drawing_spec = mp_drawing.DrawingSpec(thickness=0.5, circle_radius=0.5)
cap = cv2.VideoCapture(0)

blink_count = 0
is_closed = False
close_start_time = 0
yawn_count = 0
is_yawning = False
yawn_start_time = 0

with mp_face_mesh.FaceMesh(
  max_num_faces=2,
  refine_landmarks=True,
  min_detection_confidence=0.5,
  min_tracking_confidence=0.5) as face_mesh:
  
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    
    image = cv2.flip(image, 1)

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style())

      face = results.multi_face_landmarks[0]
      h, w, c = image.shape
      landmark_list = []
      for id, xyz_coord in enumerate(face.landmark):
        landmark_list.append([id, float(xyz_coord.x*w), float(xyz_coord.y*h), float(xyz_coord.z*h)])
        #landmark number
        #cv2.putText(image, str(id), (int(landmark_list[id][1]), int(landmark_list[id][2])), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0,),1)
      
      """x1, y1, z1 = landmark_list[129][1], landmark_list[129][2], landmark_list[129][3]
      x2, y2, z2 = landmark_list[168][1], landmark_list[168][2], landmark_list[168][3] 
      x3, y3, z3 = landmark_list[358][1], landmark_list[358][2], landmark_list[358][3]
      nx = (y2-y1)*(z3-z1)-(z2-z1)*(y3-y1)
      ny = (x2-x1)*(z3-z1)-(z2-z1)*(x3-x1)
      nz = (y2-y1)*(x3-x1)-(x2-x1)*(y3-y1)
      print(landmark_list[4])
      face_dir_vector = [nx/nz, ny/nz, 1]

      #face director vector line
      cv2.line(image, (int(landmark_list[5][1]), int(landmark_list[5][2])), (int(-nx*0.1+landmark_list[5][1]), int(ny*0.1+landmark_list[5][2])), (255,0,255), 2, cv2.LINE_4, 0)"""

      face_reference = [(landmark_list[234][1]+landmark_list[454][1])/2, (landmark_list[234][2]+landmark_list[454][2])/2, (landmark_list[234][3] + landmark_list[454][3])/2]
      face_dir_vector = [landmark_list[5][1]-face_reference[0],landmark_list[5][2]-face_reference[1], landmark_list[5][3]-face_reference[2]]
      face_dir_vector_ = [face_dir_vector[0]/face_dir_vector[2], face_dir_vector[1]/face_dir_vector[2], 1]
      cv2.line(image, (int(landmark_list[5][1]), int(landmark_list[5][2])), (int(landmark_list[5][1]-100*face_dir_vector_[0]), int(landmark_list[5][2]-100*face_dir_vector_[1])), (255,0,255), 2, cv2.LINE_4, 0)

      horizontal_angle = - np.degrees(np.arctan(face_dir_vector[0]/face_dir_vector[2]))
      vertical_angle = np.degrees(np.arctan(face_dir_vector[1]/face_dir_vector[2]))

      eye_reference = [(landmark_list[127][1]+landmark_list[356][1])/2, (landmark_list[127][2]+landmark_list[356][2])/2, (landmark_list[127][3] + landmark_list[356][3])/2]
      eye_reference_vector = [landmark_list[168][1]-eye_reference[0],landmark_list[168][2]-eye_reference[1], landmark_list[168][3]-eye_reference[2]]
      eye_reference_vector_ = [eye_reference_vector[0]/eye_reference_vector[2], eye_reference_vector[1]/eye_reference_vector[2], 1]
      cv2.line(image, (int(landmark_list[168][1]), int(landmark_list[168][2])), (int(landmark_list[168][1]-100*eye_reference_vector_[0]), int(landmark_list[168][2]-100*eye_reference_vector_[1])), (0,0,255), 2, cv2.LINE_4, 0)
      left_eye_reference = [(landmark_list[127][1]*2+landmark_list[356][1])/3, (landmark_list[127][2]*2+landmark_list[356][2])/3, (landmark_list[127][3]*2 + landmark_list[356][3])/3]
      right_eye_reference = [(landmark_list[127][1]+landmark_list[356][1]*2)/3, (landmark_list[127][2]+landmark_list[356][2]*2)/3, (landmark_list[127][3] + landmark_list[356][3]*2)/3]
      left_eye_vector = [landmark_list[468][1]-left_eye_reference[0],landmark_list[468][2]-left_eye_reference[1], landmark_list[468][3]-left_eye_reference[2]]
      right_eye_vector = [landmark_list[473][1]-right_eye_reference[0],landmark_list[473][2]-right_eye_reference[1], landmark_list[473][3]-right_eye_reference[2]]
      left_eye_vector_ = [left_eye_vector[0]/left_eye_vector[2], left_eye_vector[1]/left_eye_vector[2], 1]
      right_eye_vector_ = [right_eye_vector[0]/right_eye_vector[2], right_eye_vector[1]/right_eye_vector[2], 1]
      cv2.line(image, (int(landmark_list[468][1]), int(landmark_list[468][2])), (int(landmark_list[468][1]-100*left_eye_vector_[0]), int(landmark_list[468][2]-100*left_eye_vector_[1])), (0,0,255), 2, cv2.LINE_4, 0)
      cv2.line(image, (int(landmark_list[473][1]), int(landmark_list[473][2])), (int(landmark_list[473][1]-100*right_eye_vector_[0]), int(landmark_list[473][2]-100*right_eye_vector_[1])), (0,0,255), 2, cv2.LINE_4, 0)

      left_eye_indexes = [253, 254, 257, 258, 446, 463]
      right_eye_indexes = [23, 24, 27, 28, 226, 243]
      left_eye_x, left_eye_y, right_eye_x, right_eye_y = [], [], [], []
      for left_eye_coordinates in left_eye_indexes:
        left_eye_x.append(landmark_list[left_eye_coordinates][1])
        left_eye_y.append(landmark_list[left_eye_coordinates][2])
      for right_eye_coordinates in right_eye_indexes:
        right_eye_x.append(landmark_list[right_eye_coordinates][1])
        right_eye_y.append(landmark_list[right_eye_coordinates][2])
      left_eye_center = [np.mean(left_eye_x), np.mean(left_eye_y)]
      right_eye_center = [np.mean(right_eye_x), np.mean(right_eye_y)]
      left_eye_distance = [landmark_list[473][1]-left_eye_center[0],landmark_list[473][2]- left_eye_center[1]]
      right_eye_distance = [landmark_list[468][1]-right_eye_center[0],landmark_list[468][2]-right_eye_center[1]]

      cv2.line(image, (int(landmark_list[473][1]), int(landmark_list[473][2])), (int(left_eye_distance[0]*10+landmark_list[473][1]), int(left_eye_distance[1]*10+landmark_list[473][2])), (255,0,255), 2, cv2.LINE_4, 0)
      cv2.line(image, (int(landmark_list[468][1]), int(landmark_list[468][2])), (int(right_eye_distance[0]*10+landmark_list[468][1]), int(right_eye_distance[1]*10+landmark_list[468][2])), (255,0,255), 2, cv2.LINE_4, 0)
      blink_param1 = (landmark_list[386][2] - landmark_list[373][2])/(landmark_list[257][2] - landmark_list[254][2])
      blink_param2 = (landmark_list[385][2] - landmark_list[374][2])/(landmark_list[258][2] - landmark_list[253][2])
      blink_param3 = (landmark_list[158][2] - landmark_list[145][2])/(landmark_list[28][2] - landmark_list[23][2])
      blink_param4 = (landmark_list[159][2] - landmark_list[144][2])/(landmark_list[27][2] - landmark_list[24][2])
    
      if (blink_param1 + blink_param2 + blink_param3 + blink_param4 < 0.4) & (is_closed==False):
        close_start_time = time()
        blink_count += 1
        is_closed = True
      elif (blink_param1 + blink_param2 + blink_param3 + blink_param4 >= 0.4):
        is_closed = False
        close_start_time = 0
      if (time() - close_start_time > 1) & (is_closed == True):
        cv2.putText(image, "WAKE UP", (int(0.4*w), int(0.8*h)), cv2.FONT_HERSHEY_PLAIN, 7, (0,0,255), 7)
      
      cv2.circle(image, (int(landmark_list[13][1]),int(landmark_list[13][2])), 2, (255,0,255), cv2.FILLED)
      cv2.circle(image, (int(landmark_list[14][1]),int(landmark_list[14][2])), 2, (255,0,255), cv2.FILLED)
      cv2.circle(image, (int(landmark_list[78][1]),int(landmark_list[78][2])), 2, (255,0,255), cv2.FILLED)
      cv2.circle(image, (int(landmark_list[308][1]),int(landmark_list[308][2])), 2, (255,0,255), cv2.FILLED)

      yawn_param1 = ((landmark_list[13][1]-landmark_list[14][1])**2 + (landmark_list[13][2]-landmark_list[14][2])**2)**0.5
      yawn_param2 = ((landmark_list[308][1]-landmark_list[78][1])**2 + (landmark_list[308][2]-landmark_list[78][2])**2)**0.5

      if (yawn_param1/yawn_param2 > 0.8) & (is_yawning==False):
        yawn_start_time = time()
        is_yawning = True
      elif (yawn_param1/yawn_param2 <= 0.7):
        yawn_start_time = 0
        is_yawning = False
      if (time()-yawn_start_time > 1.5) & (is_yawning==True):
        yawn_count += 1
        is_yawning = False

      cv2.putText(image, "Blink count: {}".format(blink_count), (int(0.05*w), int(0.1*h)), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
      cv2.putText(image, "Yawn count: {}".format(yawn_count), (int(0.05*w), int(0.15*h)), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
      cv2.putText(image, "Horizontal angle : %.2f"%horizontal_angle, (int(0.05*w), int(0.2*h)), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
      cv2.putText(image, "Verticalal angle : %.2f"%vertical_angle, (int(0.05*w), int(0.25*h)), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

    cv2.imshow('MediaPipe Face Mesh', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()