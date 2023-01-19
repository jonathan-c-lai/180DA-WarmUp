import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Used code linked by professor as tutorial from here: https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
# I adapted it to instead fill in a colored rectangle at the top of the screen
# representing dominant color, as well as only finding the dominant color
# on a portion of the captured screen
# I adapted it to find dominant color from video feed
# I also used this tutorial: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
# to capture video feed

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

cap = cv2.VideoCapture(0)

while (True):
    # Take each frame
    _, frame = cap.read()

    frame_rgb = frame[100:500, 180:390]
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_rgb = frame_rgb.reshape((frame_rgb.shape[0] * frame_rgb.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(frame_rgb)

    # Get dominant color
    hist = find_histogram(clt)
    max_percent = 0
    max_color = 0
    for (percent, color) in zip(hist, clt.cluster_centers_):
        if (percent > max_percent):
            max_percent = percent
            max_color = color.astype("uint8").tolist()

    # Display the resulting frame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Fill in a rectangle representing the dominant color
    cv2.rectangle(frame, (200,5), (400,100), max_color, -1)

    # Show where the dominant color is being attempted to be captured
    cv2.rectangle(frame, (100,180), (500,390), (0,255,0), 3)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()