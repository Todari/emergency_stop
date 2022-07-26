import cv2
import mediapipe as mp
from .face import Face
from .eye import Eye

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

    self.size = [0, 0, 0]
    self.landmark_list = []

    self.face = None
    self.eye = None

    self.is_sleeping = False

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

  def drawing_face_mesh(self, results):
    for face_landmarks in results.multi_face_landmarks:
      """self.mp_drawing.draw_landmarks(
          image=self.image,
          landmark_list=face_landmarks,
          connections=self.mp_face_mesh.FACEMESH_TESSELATION,
          landmark_drawing_spec=None,
          connection_drawing_spec=self.mp_drawing_styles
          .get_default_face_mesh_tesselation_style())"""
      self.mp_drawing.draw_landmarks(
          image=self.image,
          landmark_list=face_landmarks,
          connections=self.mp_face_mesh.FACEMESH_CONTOURS,
          landmark_drawing_spec=None,
          connection_drawing_spec=self.mp_drawing_styles
          .get_default_face_mesh_contours_style())
      """self.mp_drawing.draw_landmarks(
          image=self.image,
          landmark_list=face_landmarks,
          connections=self.mp_face_mesh.FACEMESH_IRISES,
          landmark_drawing_spec=None,
          connection_drawing_spec=self.mp_drawing_styles
          .get_default_face_mesh_iris_connections_style())"""

  def init_face_eye(self):
    
    self.face = Face(self.landmark_list)
    self.eye = Eye(self.landmark_list)
    
  def drawing_face_direction(self):

    self.face.face_direction()
    self.face.face_direction2()

    cv2.line(self.image, (self.face.point1[0],self.face.point1[1]), (self.face.point2[0], self.face.point2[1]), (255,0,255), 2, cv2.LINE_4, 0)
    cv2.line(self.image, (self.face.point3[0],self.face.point3[1]), (self.face.point4[0], self.face.point4[1]), (255,0,255), 2, cv2.LINE_4, 0)
    cv2.putText(self.image, "Horizontal angle : %.2f"%self.face.horizontal_angle, (int(0.05*self.size[1]), int(0.2*self.size[0])), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
    cv2.putText(self.image, "Verticalal angle : %.2f"%self.face.vertical_angle, (int(0.05*self.size[1]), int(0.25*self.size[0])), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

  def print_yawn_counter(self):

    self.face.yawn_counter()

    cv2.putText(self.image, "Yawn count: {}".format(self.face.yawn_count), (int(0.05*self.size[1]), int(0.15*self.size[0])), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

  def print_blink_counter(self):

    self.eye.blink_counter()
    cv2.putText(self.image, "Blink count: {}".format(self.eye.blink_count), (int(0.05*self.size[1]), int(0.1*self.size[0])), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

    if self.eye.is_sleeping():
      cv2.putText(self.image, "!! WAKE UP !!", (int(0.2*self.size[1]), int(0.8*self.size[0])), cv2.FONT_HERSHEY_PLAIN, 10, (0,0,255), 5)

  def drawing_eye_direction(self):

    self.eye.eye_direction()
    
    cv2.line(self.image, (self.eye.point1[0],self.eye.point1[1]), (self.eye.point2[0], self.eye.point2[1]), (0,0,255), 2, cv2.LINE_4, 0)
    cv2.line(self.image, (self.eye.point3[0],self.eye.point3[1]), (self.eye.point4[0], self.eye.point4[1]), (0,0,255), 2, cv2.LINE_4, 0)