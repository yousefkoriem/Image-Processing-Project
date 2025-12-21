import cv2

def Gaussian(img,kernel):
  gauss = cv2.GaussianBlur(img, (kernel,kernel), 0)
  return gauss