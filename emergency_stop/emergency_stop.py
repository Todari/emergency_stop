import cv2
import mediapipe as mp
from .face import Face

class EmergencyStop():

  def __init__ (self):

    self.mp_face_mesh = mp.solutions.face_mesh
    self.mp_drawing = mp.solutions.drawing_utils
    self.mp_drawing_styles = mp.solutions.drawing_styles
    self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=0.5, circle_radius=0.5)
    
    self.face_mesh = self.mp_face_mesh.FaceMesh(
      max_num_faces = 1,
      refine_landmarks = True,
      min_detection_confidence = 0.5,
      min_tracking_confidence = 0.5
    )

    self.image = None

    self.blink_count = 0
    self.is_closed = False
    self.close_start_time = 0

    self.size = [0, 0, 0]

    self.landmark_list = []
    self.face = None

  def init(self, image):

    self.image = image
    self.image = cv2.flip(self.image, 1)
    self.image.flags.writeable = False
    self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
    
    self.image.flags.writeable = True
    self.image = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)

  def get_landmarks(self, results):

    landmarks = results.multi_face_landmarks[0]
    self.landmark_list=[]

    """size[0] = h, size[1] = w, size[2] = c"""
    self.size[0], self.size[1], self.size[2] = self.image.shape

    for id, xyz_coord in enumerate(landmarks.landmark):
      self.landmark_list.append([id, float(xyz_coord.x*self.size[1]), float(xyz_coord.y*self.size[0]), float(xyz_coord.z*self.size[0])])
      
      """show landmark number"""
      #cv2.putText(image, str(id), (int(landmark_list[id][1]), int(landmark_list[id][2])), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0,),1)

    self.face = Face(self.landmark_list)

  def drawing_face_mesh(self, results):
    for face_landmarks in results.multi_face_landmarks:
      self.mp_drawing.draw_landmarks(
          image=self.image,
          landmark_list=face_landmarks,
          connections=self.mp_face_mesh.FACEMESH_TESSELATION,
          landmark_drawing_spec=None,
          connection_drawing_spec=self.mp_drawing_styles
          .get_default_face_mesh_tesselation_style())
      self.mp_drawing.draw_landmarks(
          image=self.image,
          landmark_list=face_landmarks,
          connections=self.mp_face_mesh.FACEMESH_CONTOURS,
          landmark_drawing_spec=None,
          connection_drawing_spec=self.mp_drawing_styles
          .get_default_face_mesh_contours_style())
      self.mp_drawing.draw_landmarks(
          image=self.image,
          landmark_list=face_landmarks,
          connections=self.mp_face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=self.mp_drawing_styles
          .get_default_face_mesh_iris_connections_style())
    

  def drawing_face_direction(self):

    self.face.face_direction()

    cv2.line(self.image, (self.face.point1[0],self.face.point1[1]), (self.face.point2[0], self.face.point2[1]), (255,0,255), 2, cv2.LINE_4, 0)
    cv2.putText(self.image, "Horizontal angle : %.2f"%self.face.horizontal_angle, (int(0.05*self.size[1]), int(0.2*self.size[0])), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
    cv2.putText(self.image, "Verticalal angle : %.2f"%self.face.vertical_angle, (int(0.05*self.size[1]), int(0.25*self.size[0])), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

  def print_yawn_counter(self):

    self.face.yawn_counter()

    cv2.putText(self.image, "Yawn count: {}".format(self.face.yawn_count), (int(0.05*self.size[1]), int(0.15*self.size[0])), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)





  #       eye_reference = [(landmark_list[127][1]+landmark_list[356][1])/2, (landmark_list[127][2]+landmark_list[356][2])/2, (landmark_list[127][3] + landmark_list[356][3])/2]
  #       eye_reference_vector = [landmark_list[168][1]-eye_reference[0],landmark_list[168][2]-eye_reference[1], landmark_list[168][3]-eye_reference[2]]
  #       eye_reference_vector_ = [eye_reference_vector[0]/eye_reference_vector[2], eye_reference_vector[1]/eye_reference_vector[2], 1]
  #       cv2.line(image, (int(landmark_list[168][1]), int(landmark_list[168][2])), (int(landmark_list[168][1]-100*eye_reference_vector_[0]), int(landmark_list[168][2]-100*eye_reference_vector_[1])), (0,0,255), 2, cv2.LINE_4, 0)
  #       left_eye_reference = [(landmark_list[127][1]*2+landmark_list[356][1])/3, (landmark_list[127][2]*2+landmark_list[356][2])/3, (landmark_list[127][3]*2 + landmark_list[356][3])/3]
  #       right_eye_reference = [(landmark_list[127][1]+landmark_list[356][1]*2)/3, (landmark_list[127][2]+landmark_list[356][2]*2)/3, (landmark_list[127][3] + landmark_list[356][3]*2)/3]
  #       left_eye_vector = [landmark_list[468][1]-left_eye_reference[0],landmark_list[468][2]-left_eye_reference[1], landmark_list[468][3]-left_eye_reference[2]]
  #       right_eye_vector = [landmark_list[473][1]-right_eye_reference[0],landmark_list[473][2]-right_eye_reference[1], landmark_list[473][3]-right_eye_reference[2]]
  #       left_eye_vector_ = [left_eye_vector[0]/left_eye_vector[2], left_eye_vector[1]/left_eye_vector[2], 1]
  #       right_eye_vector_ = [right_eye_vector[0]/right_eye_vector[2], right_eye_vector[1]/right_eye_vector[2], 1]
  #       cv2.line(image, (int(landmark_list[468][1]), int(landmark_list[468][2])), (int(landmark_list[468][1]-100*left_eye_vector_[0]), int(landmark_list[468][2]-100*left_eye_vector_[1])), (0,0,255), 2, cv2.LINE_4, 0)
  #       cv2.line(image, (int(landmark_list[473][1]), int(landmark_list[473][2])), (int(landmark_list[473][1]-100*right_eye_vector_[0]), int(landmark_list[473][2]-100*right_eye_vector_[1])), (0,0,255), 2, cv2.LINE_4, 0)

  #       left_eye_indexes = [253, 254, 257, 258, 446, 463]
  #       right_eye_indexes = [23, 24, 27, 28, 226, 243]
  #       left_eye_x, left_eye_y, right_eye_x, right_eye_y = [], [], [], []
  #       for left_eye_coordinates in left_eye_indexes:
  #         left_eye_x.append(landmark_list[left_eye_coordinates][1])
  #         left_eye_y.append(landmark_list[left_eye_coordinates][2])
  #       for right_eye_coordinates in right_eye_indexes:
  #         right_eye_x.append(landmark_list[right_eye_coordinates][1])
  #         right_eye_y.append(landmark_list[right_eye_coordinates][2])
  #       left_eye_center = [np.mean(left_eye_x), np.mean(left_eye_y)]
  #       right_eye_center = [np.mean(right_eye_x), np.mean(right_eye_y)]
  #       left_eye_distance = [landmark_list[473][1]-left_eye_center[0],landmark_list[473][2]- left_eye_center[1]]
  #       right_eye_distance = [landmark_list[468][1]-right_eye_center[0],landmark_list[468][2]-right_eye_center[1]]

  #       cv2.line(image, (int(landmark_list[473][1]), int(landmark_list[473][2])), (int(left_eye_distance[0]*10+landmark_list[473][1]), int(left_eye_distance[1]*10+landmark_list[473][2])), (255,0,255), 2, cv2.LINE_4, 0)
  #       cv2.line(image, (int(landmark_list[468][1]), int(landmark_list[468][2])), (int(right_eye_distance[0]*10+landmark_list[468][1]), int(right_eye_distance[1]*10+landmark_list[468][2])), (255,0,255), 2, cv2.LINE_4, 0)
  #       blink_param1 = (landmark_list[386][2] - landmark_list[373][2])/(landmark_list[257][2] - landmark_list[254][2])
  #       blink_param2 = (landmark_list[385][2] - landmark_list[374][2])/(landmark_list[258][2] - landmark_list[253][2])
  #       blink_param3 = (landmark_list[158][2] - landmark_list[145][2])/(landmark_list[28][2] - landmark_list[23][2])
  #       blink_param4 = (landmark_list[159][2] - landmark_list[144][2])/(landmark_list[27][2] - landmark_list[24][2])
      
  #       if (blink_param1 + blink_param2 + blink_param3 + blink_param4 < 0.4) & (is_closed==False):
  #         close_start_time = time()
  #         blink_count += 1
  #         is_closed = True
  #       elif (blink_param1 + blink_param2 + blink_param3 + blink_param4 >= 0.4):
  #         is_closed = False
  #         close_start_time = 0
  #       if (time() - close_start_time > 1) & (is_closed == True):
  #         cv2.putText(image, "WAKE UP", (int(0.4*w), int(0.8*h)), cv2.FONT_HERSHEY_PLAIN, 7, (0,0,255), 7)
        
  #       cv2.circle(image, (int(landmark_list[13][1]),int(landmark_list[13][2])), 2, (255,0,255), cv2.FILLED)
  #       cv2.circle(image, (int(landmark_list[14][1]),int(landmark_list[14][2])), 2, (255,0,255), cv2.FILLED)
  #       cv2.circle(image, (int(landmark_list[78][1]),int(landmark_list[78][2])), 2, (255,0,255), cv2.FILLED)
  #       cv2.circle(image, (int(landmark_list[308][1]),int(landmark_list[308][2])), 2, (255,0,255), cv2.FILLED)

  #       yawn_param1 = ((landmark_list[13][1]-landmark_list[14][1])**2 + (landmark_list[13][2]-landmark_list[14][2])**2)**0.5
  #       yawn_param2 = ((landmark_list[308][1]-landmark_list[78][1])**2 + (landmark_list[308][2]-landmark_list[78][2])**2)**0.5

  #       if (yawn_param1/yawn_param2 > 0.8) & (is_yawning==False):
  #         yawn_start_time = time()
  #         is_yawning = True
  #       elif (yawn_param1/yawn_param2 <= 0.7):
  #         yawn_start_time = 0
  #         is_yawning = False
  #       if (time()-yawn_start_time > 1.5) & (is_yawning==True):
  #         yawn_count += 1
  #         is_yawning = False

  #       cv2.putText(image, "Blink count: {}".format(blink_count), (int(0.05*w), int(0.1*h)), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
  #       cv2.putText(image, "Yawn count: {}".format(yawn_count), (int(0.05*w), int(0.15*h)), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
        

  #     cv2.imshow('MediaPipe Face Mesh', image)
  #     if cv2.waitKey(5) & 0xFF == 27:
  #       break
  # cap.release()