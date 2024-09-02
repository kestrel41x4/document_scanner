import numpy as np
import cv2
import matplotlib.pyplot as plt
import imutils
from imutils.perspective import four_point_transform


def resizer(image,width=500):
    h,w,c = image.shape
    
    height = int((h/w)* width )
    size = (width,height)
    image = cv2.resize(image,(width,height))
    return image, size

def document_scanner(image):

    img_re,size = resizer(image)


    detail = cv2.detailEnhance(img_re,sigma_s = 20, sigma_r = 0.15)
    gray = cv2.cvtColor(detail,cv2.COLOR_BGR2GRAY) # GRAYSCALE IMAGE
    blur = cv2.GaussianBlur(gray,(5,5),0)
    # edge detect
    edge_image = cv2.Canny(blur,75,200)
    # morphological transform
    kernel = np.ones((5,5),np.uint8)
    dilate = cv2.dilate(edge_image,kernel,iterations=1)

    closing = cv2.morphologyEx(dilate,cv2.MORPH_CLOSE,kernel)

    contours , hire = cv2.findContours(closing,
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour,0.02*peri, True)

        if len(approx) == 4:
            four_points = np.squeeze(approx)
            break

    cv2.drawContours(img_re, [four_points],-1,(0,255,0),3)


    multiplier = image.shape[1] / size[0]
    four_points_orig = four_points * multiplier
    four_points_orig = four_points_orig.astype(int)

    warp_image = four_point_transform(image,four_points_orig)

    return warp_image, four_points_orig, img_re, closing


img = cv2.imread('./images/')
wrpimg, points, cnt_img, edgeimg = document_scanner(img)
cv2.imshow('img', img)
cv2.imshow('warp', cnt_img)
cv2.imshow('resize', edgeimg)
cv2.imshow('warp', wrpimg)
cv2.waitKey(0)
cv2.destroyAllWindows()