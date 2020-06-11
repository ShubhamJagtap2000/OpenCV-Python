import cv2
import imutils
from imutils.perspective import four_point_transform
from imutils import contours

#define the dictionary of 7-segment display
DIGITS_LOOKUP = {
    (1,1,1,0,1,1,1):0,
    (0,0,1,0,0,1,0):1,
    (1,0,1,1,1,1,0):2,
    (1,0,1,1,0,1,1):3,
    (0,1,1,1,0,1,0):4,
    (1,1,0,1,0,1,1):5,
    (1,1,0,1,1,1,1):6,
    (1,0,1,0,0,1,0):7,
    (1,1,1,1,1,1,1):8,
    (1,1,1,1,0,1,1):9,
    }
#image pre-processing
img = cv2.imread('digitRecognition.jpg')
img = imutils.resize(img,height = 500)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(img,(5,5),0)
edged = cv2.Canny(blurred,50,200)
#cv2.imshow('image',img)
#cv2.imshow('edged',edged)

#find contours and sort them acc to their size in decreasing order
cnts = cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts,key=cv2.contourArea,reverse=True)
displayCnt = None
for c in cnts:
    #contour approximation
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.02*peri,True)
    #if contour has 4 vertices,we have found the digital display
    if len(approx) == 4:
        displayCnt = approx
        break
#extract display
warped = four_point_transform(gray,displayCnt.reshape(4,2))
output = four_point_transform(img,displayCnt.reshape(4,2))
#cv2.imshow('warped',warped)
#threshold the image and apply morphlogical transforms to clean-up the image
thresh = cv2.threshold(warped,127,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,5))
thresh = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel)
#cv2.imshow('thresholded',thresh)
#find contours in the thresholded image and initialize the digit contour list
cnts = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
digitCnts = []
for c in cnts:
    #bounding box of the contour
    (x,y,w,h) = cv2.boundingRect(c)
    #if box is in the respective range then it is a digit
    if w>=15 and (h>=30 and h<=40):
        digitCnts.append(c)
#initialize the digit contour list and place in the order
digitCnts = contours.sort_contours(digitCnts,method = "left-to-right")[0]
digits = []
#loop for each digit
for c in digitCnts:
    #set ROI of each digit
    (x,y,w,h) = cv2.boundingRect(c)
    roi = thresh[y:y+h,x:x+w]
    #set dimensions of each digit
    (roiH,roiW) = roi.shape
    (dW,dH) = (int(roiW*0.25),int(roiH*0.15))
    dHC = int(roiH*0.05)
    #define the 7-segments
    segments = [
        ((0,0),(w,dH)), #top
        ((0,0),(dW,h//2)),  #top-left
        ((w - dW,0),(w,h//2)),  #top-right
        ((0,(h//2)-dHC),(w,(h//2)+dHC)),   #center
        ((0,h//2),(dW,h)),  #bottom-left
        ((w-dW,h//2),(w,h)),    #bottom-right
        ((0,h-dH),(w,h))   #bottom
        ]
    #look if the segment is on/off
    on = [0]*len(segments)
    #lookup for each digit in ROI
    for (i,((xA,yA),(xB,yB))) in enumerate(segments):
        segROI = roi[yA:yB,xA:xB]
        total = cv2.countNonZero(segROI)
        area = (xB - xA)*(yB - yA)
        if total/float(area) > 0.5:
            on[i] = 1
    digit = DIGITS_LOOKUP[tuple(on)]
    digits.append(digit)
    cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),1)
    cv2.putText(output,str(digit),(x - 10,y - 10),cv2.FONT_HERSHEY_SIMPLEX,0.65,(0,255,0),2)
    
print(u"{}{}.{}\u00b0c".format(*digits))
cv2.imshow("INPUT",img)
cv2.imshow("OUTPUT",output)
cv2.waitKey(0)
cv2.destroyAllWindows()

    
    
