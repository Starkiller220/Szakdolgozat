import cv2
import pytesseract
import numpy as np
import time,zmq,os,math
from skimage.morphology import skeletonize

class WarcraftAI:
    def __init__(self):
        self.lumber = 0
        self.gold = 0
        self.map = np.zeros(shape=(64,64))
        self.offset = None

        self.context = zmq.Context()
        print("Connecting to dosbox...")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")
        np.set_printoptions(threshold=np.inf)
        self.MainLoop()


    def TemplateMatching(self,playArea):

        img_gray = cv2.cvtColor(playArea, cv2.COLOR_BGR2GRAY)

        units = [
                ['./program/imgs/footman',(255,0,0),0.82,1],
                ['./program/imgs/peasant',(0,100,255),0.9,2],
                ['./program/imgs/buildings',(0,255,255),0.76,3],
                ['./program/imgs/tree',(19,69,139),0.8,4]
                ]

        for unit in units:
            for filename in os.listdir(unit[0]):
                
                template = cv2.imread(f"{unit[0]}/{filename}",0)
                w, h = template.shape[::-1]
                for i in range(2):
                    template = cv2.flip(template,1)
                    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                    threshold = unit[2]
                    loc = np.where( res >= threshold)

                    for pt in zip(*loc[::-1]):
                        #print(pt)
                        #print(f"{math.ceil(pt[1] / 16)},{math.ceil(pt[0] / 16)}")
                        if self.offset != None:
                            #print(self.offset[0]+math.ceil(pt[1] / 16))
                            self.map[self.offset[0]+math.ceil(pt[1] / 16)][self.offset[1]+math.ceil(pt[0] / 16)] = 2
                        cv2.rectangle(playArea, pt, (pt[0] + w, pt[1] + h), unit[1], 2)
                        cv2.imwrite('res.png',playArea)

        

    def ReadText(self,name: str,cropImage: np.ndarray):

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
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4,6)) # can be tweaked
            skeleton_dilated = ~cv2.morphologyEx(skeleton, cv2.MORPH_DILATE, kernel)

            data = pytesseract.image_to_string(skeleton_dilated, lang='eng',config='--psm 10 -c tessedit_char_whitelist=0123456789s')
            print(f"{name}: "+data.replace("$","8").replace("o","0").replace("s","5").replace("i","1"))

            #cv2.imshow('thresh', thresh)
            #cv2.imshow('img', img)
            cv2.imwrite(f"{name}.png",skeleton_dilated)
            return

    def GetOffset(self,cropMap):
        for i in range(64):
            for j in range(64):
                if(list(cropMap[i][j]) == [199,199,199]):
                    return (j,i)
        return None

    def UpdateMap(self,cropMap):
        self.offset = self.GetOffset(cropMap)
        print(self.offset)
        

    def MainLoop(self):
        while True:
        
            pytesseract.pytesseract.tesseract_cmd = r"C:\Programs\Tesseract-OCR\tesseract.exe" # Need to be dynamic

            image = cv2.imread('C:\\Users\\Kriszu\\Desktop\\capture\\war_000.png')
            
            try:
                self.ReadText("Lumber",image[1:8,143:169])
                self.ReadText("Gold",image[1:8,243:269])       
                cv2.imwrite("map.png",image[6:70,3:67]) # térkép
                cv2.imwrite("playArea.png",image[12:188,72:312]) #játéktér

            except TypeError:
                continue

            self.UpdateMap(image[6:70,3:67])
            self.TemplateMatching(image[12:188,72:312])

            self.socket.send(bytes("Mouse 230 100",'utf-8'))
            message = self.socket.recv()
            print(f"Received reply {message}")
            
            #cv2.waitKey()
            time.sleep(0.5)