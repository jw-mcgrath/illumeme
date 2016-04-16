import cv2

def find_triangles(filename):
    FIRST = 0
    RED = (0, 0, 255)
    THICKNESS = 3
    copy = img = cv2.imread(filename)
    grey_img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
    ret, thresh = cv2.threshold(grey_img, 127, 255, 1)
    contours, h = cv2.findContours(thresh, 1, 2)
    largest = None
    for contour in countours:
        approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
        if len(approx) == 3:
            #triangle found
            if largest is None or cv2.contourArea(contour) > cv2.contourArea(largest):
                largest = contour
   
    #write file
    cv2.drawContours(copy, [largest], FIRST, RED, THICKNESS)
    cv2.imwrite(filename +"_result", copy)

find_trianlges("picture")
