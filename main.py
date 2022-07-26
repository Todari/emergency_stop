import cv2
from emergency_stop import EmergencyStop

ES = EmergencyStop()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("카메라가 인식되지 않습니다.")
        continue

    ES.init(image)
    results = ES.face_mesh.process(ES.image)

    if results.multi_face_landmarks:
        ES.drawing_face_mesh(results)
        ES.get_landmarks(results)
        ES.drawing_face_direction()
        ES.print_yawn_counter()
    
    cv2.imshow("Emergency stop", ES.image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()