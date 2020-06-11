import cv2
import numpy as np

def order_points(pts):
    '''initialzie a list of coordinates that will be ordered
    such that the first entry in the list is the top-left,
    the second entry is the top-right, the third is the
    bottom-right, and the fourth is the bottom-left'''
    rect = np.zeros((4, 2), dtype = "float32")
    '''the top-left point will have smallest sum,whereas the bottom-right
    point will have the largest sum'''
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    '''now,compute difference between points,the top-right point will have
    smallest difference and bottom-right will have largest'''
    diff = np.diff(pts,axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmin(diff)]
    #return the ordered coordinates
    return rect

def four_point_transform(image,pts):
    rect = order_points(pts)
    (tl,tr,br,bl) = rect
    '''compute the width of new image,which will be the max distance between
    top-right and bottom-right y-coordinates or the top-left and bottom-left
    x-coordinates'''
    widthA = np.sqrt(((br[0]-bl[0])**2) + ((br[1]-bl[1])**2))
    widthB = np.sqrt(((tr[0]-tl[0])**2) + ((tr[1]-tl[1])**2))
    maxWidth = max(int(widthA),int(widthB))
    '''compute the width of new image,which will be the max distance between
    top-right and bottom-right y-coordinates or the top-left and bottom-left
    x-coordinates'''
    heightA = np.sqrt(((tr[0]-br[0])**2) + ((tr[1]-br[1])**2))
    heightB = np.sqrt(((tl[0]-bl[0])**2) + ((tl[1]-bl[1])**2))
    maxHeight = max(int(HeightA),int(HeightB))
    #now set the destination points to get top-down view of image
    dst = np.array([[0,0],[maxWidth-1,0],[maxHeight-1,maxHeight-1],
                    [0,maxHeight-1]],dtype = "float32")
    #compute perspective transform matrix and perform it
    M = cv2.getPerspectiveTransform(rect,dst)
    warped = cv2.warpPerspective(image,M,(maxidth,maxHeight))
    return warped

        
