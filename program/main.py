import cv2
import pytesseract
import numpy as np
import time
import zmq
from skimage.morphology import skeletonize

def ReadText(name: str,cropImage: np.ndarray):

        if cropImage is None:
            return

        scale_percent = 600 # percent of original size
        width = int(cropImage.shape[1] * scale_percent / 100)
        height = int(cropImage.shape[0] * scale_percent / 100)
        dimension = (width, height)

        # resize image
        res = cv2.resize(cropImage, dimension, interpolation = cv2.INTER_AREA)
        # convert to gray
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        # threshold image
        thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        skeleton = cv2.threshold(thresh,0,1,cv2.THRESH_BINARY)[1]
        skeleton = (255*skeletonize(skeleton)).astype(np.uint8)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,6)) # can be tweaked
        skeleton_dilated = ~cv2.morphologyEx(skeleton, cv2.MORPH_DILATE, kernel)

        data = pytesseract.image_to_string(skeleton_dilated, lang='eng',config='--psm 10 -c tessedit_char_whitelist=0123456789s')
        print(f"{name}: "+data.replace("$","8").replace("o","0").replace("s","5").replace("i","1"))

        #cv2.imshow('thresh', thresh)
        #cv2.imshow('img', img)
        cv2.imwrite(f"{name}.png",skeleton_dilated)
        

def Main():

    context = zmq.Context()
    print("Connecting to dosbox...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    while True:

        pytesseract.pytesseract.tesseract_cmd = r"C:\Programs\Tesseract-OCR\tesseract.exe" # Need to be dynamic

        image = cv2.imread('war_000.png')
        
        ReadText("Lumber",image[1:8,143:169])
        ReadText("Gold",image[1:8,243:269])
        
        socket.send(bytes("teszt",'utf-8'))
        message = socket.recv()
        print(f"Received reply {message}")

        #cv2.waitKey()
        time.sleep(1)

Main()