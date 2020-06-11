import cv2
import numpy as np

drawing = False     #true if mouse is pressed
mode = True     #if true,draw rectangle.Press 'm' to toggle to curve
ix,iy = -1,-1

#mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing,mode

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),0)
            else:
                cv2.circle(img,(x,y),10,(255,0,0),-1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv2.rectangle(img,(ix,iy),(x,y),(0,255,0),0)
        else:
            cv2.circle(img,(x,y),10,(255,0,0),-1)

img = np.zeros((1024,1024,3),np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
    cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
            break

    def nothing(x):
        pass

    #create a black image,a window
    img = np.zeros((512,512,3),np.uint8)
    cv2.namedWindow('image')

    #create trackbars for color change
    cv2.createTrackbar('B','image',0,255,nothing)
    cv2.createTrackbar('G','image',0,255,nothing)
    cv2.createTrackbar('R','image',0,255,nothing)

    #create switch for ON/OFF functionality
    switch = 'ON/OFF'
    cv2.createTrackbar(switch,'image',0,1,nothing)

    while(1):
        cv2.imshow('image',img)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
        #get current positions of four trackbars
        b = cv2.getTrackbarPos('B','image')
        g = cv2.getTrackbarPos('G','image')
        r = cv2.getTrackbarPos('R','image')
        s = cv2.getTrackbarPos(switch,'image')

        if s == 0:
            img[:] = 0
        else:
            img[:] = [b,g,r]

cv2.destroyAllWindows()        
