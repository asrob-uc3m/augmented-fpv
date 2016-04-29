import numpy as np
import cv2
from time import sleep as slp
cap = cv2.VideoCapture(0)

x = 1

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    x = x * (-1)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if x > 0:
        gray = cv2.flip(gray, 1)



    # Display the resulting frame
    cv2.imshow('frame',gray)
    # cmd + Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
