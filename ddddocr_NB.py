import cv2
import numpy as np
import ddddocr
def free(filepath):
    # 灰度化
    im = cv2.imread(filepath)
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite('qrcode_temp.png',im_gray)
    # 高斯模糊
    ret, im_inv = cv2.threshold(im_gray,250,255,cv2.THRESH_BINARY_INV)
    # cv2.imwrite('qrcode_temp.png',im_inv)
    # 二值化
    kernel = 1/16*np.array([[1,2,1], [2,4,2], [1,2,1]])
    im_blur = cv2.filter2D(im_inv,-1,kernel)
    cv2.imwrite('qrcode_temp1.png',im_blur)
    ocr = ddddocr.DdddOcr()
    with open('qrcode_temp1.png', 'rb') as f:
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    code=res
    return code



