import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    ret,gray = cap1.read()
    cv2.imshow('frame',frame)
    cv2.imshow('gray',gray)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cap.release()
cap1.release()
cv2.destroyAllWindows()
        
