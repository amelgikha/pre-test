import cv2

image = cv2.imread('a.jpg',0)
cv2.imshow("grayimage", image)
cv2.waitKey(0)
cv2.destroyAllWindows()