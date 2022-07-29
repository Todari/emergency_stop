import cv2
from emergency_stop import EmergencyStop
from multiprocessing import Process

ES = EmergencyStop()
cap = cv2.VideoCapture(0)
p_sleeping_sound = Process(target=ES.sleeping_sound)
p_direction_sound = Process(target=ES.direction_sound)

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

        ES.init_face_eye()
        ES.drawing_face_direction()
        ES.print_yawn_counter()
        ES.print_blink_counter()
        ES.print_looking_direction()
        
        if ES.sleeping_alert() & (ES.playing_sleeping_sound==False):
            ES.playing_sleeping_sound = True
            p_sleeping_sound.start()
            print("sleeping", ES.playing_sleeping_sound)
        if ES.direction_alert() & (ES.playing_direction_sound==False):
            ES.playing_direction_sound = True
            p_direction_sound.start()
            print("direction", ES.playing_direction_sound)
    
    cv2.imshow("Emergency stop", ES.image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()