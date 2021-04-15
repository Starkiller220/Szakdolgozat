import cv2
import pytesseract
import numpy as np
import time,zmq,os,math,random
from skimage.morphology import skeletonize

class WarcraftAI:
    def __init__(self):
        self.lumber = 0
        self.gold = 0
        self.map = [np.zeros(shape=(64,64)),np.zeros(shape=(64,64)),np.zeros(shape=(64,64))] # 0 -> resources 1 -> exploration 2-> buildings
        self.offset = None
        self.commands = []
        self.stage = 0

        self.context = zmq.Context()
        print("Connecting to dosbox...")
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")
        self.MainLoop()


    def TemplateMatching(self,playArea):
        self.map[0] = np.zeros(shape=(64,64))
        self.map[2] = np.zeros(shape=(64,64))
        img_gray = cv2.cvtColor(playArea, cv2.COLOR_BGR2GRAY)

        units = [
                Unit('./imgs/footman',(255,0,0),0.82,1,1),
                Unit('./imgs/peasant',(0,100,255),0.9,0,1),
                Unit('./imgs/buildings',(0,255,255),0.76,2,1),
                Unit('./imgs/tree',(19,69,139),0.8,0,2)
                ]

        for unit in units:
            for filename in os.listdir(unit.location):
                
                template = cv2.imread(f"{unit.location}/{filename}",0)
                w, h = template.shape[::-1]
                for i in range(2):
                    template = cv2.flip(template,1)
                    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                    threshold = unit.threshold
                    loc = np.where( res >= threshold)

                    for pt in zip(*loc[::-1]):
                        if self.offset != None:
                            if(unit.mapmode == 2):
                                self.map[unit.mapmode][self.offset[0]+math.ceil(pt[1] / 16)][self.offset[1]+math.ceil(pt[0] / 16)] = int(filename[:len(filename)-4])
                            else:
                                self.map[unit.mapmode][self.offset[0]+math.ceil(pt[1] / 16)][self.offset[1]+math.ceil(pt[0] / 16)] = unit.id
                        cv2.rectangle(playArea, pt, (pt[0] + w, pt[1] + h), unit.color, 2)
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
        for i in range(64):
            for j in range(64):
                if(list(cropMap[i][j]) == [0,0,0]):
                    self.map[1][i][j] = -1
                elif(list(cropMap[i][j]) == [255,0,0]):
                    self.map[1][i][j] = 100
        
    def GatherPhase(self):
        peasants = []
        trees = []
        mines = []

        for i in range(64):
            for j in range(64):
                if(self.map[0][i][j] == 1):
                    peasants.append([i,j])
                elif(self.map[0][i][j] == 2):
                    trees.append([i,j])

        for peasant in peasants:           
            if(len(trees) > 0):
                self.commands.append(f"Gather {self.GetClickCoord(peasant[0],peasant[1],1)} { self.GetClickCoord(trees[0][0],trees[0][1],0)}")

    def ExplorePhase(self):

        footmans=[]
        target = None
        
        for i in range(64):
            for j in range(64):
                if(self.map[1][i][j] == 1):
                    footmans.append([i,j])

        if(self.offset != None):
            for i in range(self.offset[0],self.offset[0]+11):
                for j in range(self.offset[1],self.offset[1]+15):
                    if(self.map[1][i][j] == -1):           
                        target = [i,j]
                        if (random.randint(0,1) == 1):
                            break

        if(len(footmans) > 0):
            self.commands.append(f"Move {self.GetClickCoord(footmans[0][0],footmans[0][1],0)} { self.GetClickCoord(target[0],target[1],0) }")

    def BuildPhase(self):
        pass

    def TrainPhase(self):
        for i in range(64):
            for j in range(64):
                if(self.map[2][i][j] == 1):
                    pass

    def CombatPhase(self):
        pass

    def GetClickCoord(self,x,y,z):
        x -= self.offset[0]+z
        y -= self.offset[1]+z

        return f"{160+y*32} {20+x*16}"

    def ClickOnMinimap(self,x,y):
        self.commands.append(f"Click {2*x+6} {y+6}")

    def NextStage(self):
        self.stage += 1
        if self.stage > 4:
            self.stage = 0      

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
            
            if(self.stage == 0):           
                self.GatherPhase()
            elif(self.stage == 1):
                self.ExplorePhase()
            elif(self.stage == 2):
                self.TrainPhase()
            elif(self.stage == 3):
                self.CombatPhase()
            
            if(len(self.commands) != 0):
                self.socket.send(bytes(self.commands[0],'utf-8'))
                self.commands.remove(self.commands[0])
            else:
                self.socket.send(bytes(f"Skip",'utf-8'))

            #self.socket.send(bytes(f"Click {6+128} {6+64}",'utf-8'))

            self.NextStage()
            message = self.socket.recv()
            print(f"Received reply {message}")
            
            #cv2.waitKey()
            time.sleep(1)

class Unit:
    def __init__(self,location,color,threshold,mapmode,_id):
        self.location = location
        self.color = color
        self.threshold = threshold
        self.mapmode = mapmode
        self.id = _id