import cv2
from deepface import DeepFace
import numpy as np


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
video = cv2.VideoCapture('./output/output_3.mp4')



while True:
    # Read the frame
    ret, frame = video.read()
    result = DeepFace.analyze(frame, actions = ['emotion'], enforce_detection = False)
    print(result)
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(frame, result['dominant_emotion'], (50,50), font, 3, (0,0,255),2,cv2.LINE_4)
    
    # Display
    cv2.imshow('Original Video', frame)
    # Stop if esvideoe key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
# Release the VideoCapture object
video.release()
cv2.destroyAllWindows()