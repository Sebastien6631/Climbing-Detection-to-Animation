import cv2
import mediapipe as mp
import numpy as np
import time
import csv

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

#Source: https://github.com/google/mediapipe/blob/master/docs/solutions/pose.md

pTime = 0

# For webcam input:
#cap = cv2.VideoCapture(0)

# For Video input:
cap = cv2.VideoCapture('video/test1.mp4')

#create position list 
Landmark_list = []

# Ouvrez un fichier CSV en mode écriture pour enregistrer les données de mouvement
with open("pose_landmarks.txt", 'a') as txtfile:

    frame_number = 0  # Compteur de frames
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                break

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # Resize the image to a smaller size (e.g., 50% of its original size)
            # scale_percent = 50  # Adjust this value as needed
            # width = int(image.shape[1] * scale_percent / 100)
            # height = int(image.shape[0] * scale_percent / 100)
            # image = cv2.resize(image, (width, height))

            # Combine the original image with the resized image containing the landmarks
            # image[:height, :width] = image

            # Enregistrez les données de landmarks de pose dans le fichier CSV
            image_height, image_width, _ = image.shape
            pose_landmarks = results.pose_landmarks
            
            if pose_landmarks:
                lmString = ""
                for landmark_id, landmark in enumerate(pose_landmarks.landmark):
                    frame_data = {
                        'Landmark_X': landmark.x*image_width,
                        'Landmark_Y': image_height - landmark.y*image_height,  #mettre le repère en bas à gauche pour Unity
                        'Landmark_Z': landmark.z*image_height
                    }
                    
                    #register position in a string
                    lmString += f'{int(landmark.x*image_width)},{int(image_height - landmark.y*image_height)},{int(landmark.z*image_height)},'

                #register all the position in the list
                Landmark_list.append(lmString)

            print(len(Landmark_list))
            # Dessinez la pose annotation sur l'image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())            

            # print(image.shape)
            cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

            frame_number += 1  # Incrémente le compteur de frames

    #register all the landmark position in a txtfile
    for item in Landmark_list:
        txtfile.write("%s\n" % item)

cap.release()
cv2.destroyAllWindows()
