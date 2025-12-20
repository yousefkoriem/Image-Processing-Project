from filters.smooth.median import median

import pages.Noise as Noise

def main():
    print("Hello from project!")
    img = cv2.imread('sample.jpg')
    out = median(img, ksize=5)
    exp = cv2.imwrite('output.jpg', out)
    Noise.printer()

if __name__ == "__main__":
    main()
