import numpy as np
import cv2

# taken from tutorial: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
# modified to read each frame and then process each frame
# to create a mask of some color
# Used code from: https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
# to actually create the mask of image from frame
# adapted to instead of using a png, use frame from live video stream, then 
# put a bounding box over color on the screen
# used code from: https://automaticaddison.com/real-time-object-tracking-using-opencv-and-a-webcam/?fbclid=IwAR2XmZvm4rbxvX-4q5D7OKj85rDFT_eQL_6HS0FchaoEtZc93Dpn6hhyrp8
# to calculate the largest colored area and bound it with a box

cap = cv2.VideoCapture(0)

while(True):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # define range of blue color in RGB
    lower_blue = np.array([0,0,150])
    upper_blue = np.array([100,100,255])

    # Threshold the RGB image to get only blue colors
    mask = cv2.inRange(rgb, lower_blue, upper_blue)

    mask_large = mask
    contours, hierarchy = cv2.findContours(mask_large, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    areas = [cv2.contourArea(c) for c in contours]

    # if no contours
    if len(areas) < 1:
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        continue
    else:
        # find the largest moving object in the image
        max_index = np.argmax(areas)

    cnt = contours[max_index]
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()