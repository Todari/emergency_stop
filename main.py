import cv2
from emergency_stop import EmergencyStop
from multiprocessing import Process
import asyncio
from threading import Thread

ES = EmergencyStop()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("cannot detect camera")
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
            Thread(target = ES.sleeping_sound, args=(), daemon=True).start()
        if ES.direction_alert() & (ES.playing_direction_sound==False):
            ES.playing_direction_sound = True
            Thread(target = ES.direction_sound, args=(), daemon=True).start()

    
    cv2.imshow("Emergency stop", ES.image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()