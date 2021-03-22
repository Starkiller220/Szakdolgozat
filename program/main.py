import cv2
import pytesseract
import numpy as np
import time
import zmq
import os
from skimage.morphology import skeletonize

def TemplateMatching():

    for filename in os.listdir("./program/imgs/footman"):
        img_rgb = cv2.imread('playArea.png')
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(f"./program/imgs/footman/{filename}",0)
        w, h = template.shape[::-1]
        for i in range(2):
            template = cv2.flip(template,1)
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                cv2.imwrite('res.png',img_rgb)

        

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
        return
        

def Main():

    context = zmq.Context()
    print("Connecting to dosbox...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    
    while True:

        pytesseract.pytesseract.tesseract_cmd = r"C:\Programs\Tesseract-OCR\tesseract.exe" # Need to be dynamic

        image = cv2.imread('C:\\Users\\Kriszu\\Desktop\\capture\\war_000.png')
        
        ReadText("Lumber",image[1:8,143:169])
        ReadText("Gold",image[1:8,243:269])
        cv2.imwrite("map.png",image[6:70,3:67]) # térkép
        cv2.imwrite("playArea.png",image[11:189,71:313]) #játéktér

        socket.send(bytes("teszt",'utf-8'))
        message = socket.recv()
        print(f"Received reply {message}")
        TemplateMatching()
        #cv2.waitKey()
        time.sleep(0.5)

Main()