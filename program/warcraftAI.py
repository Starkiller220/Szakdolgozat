import cv2
import pytesseract
import numpy as np
import time,zmq,os,math,random
from skimage.morphology import skeletonize
from config import Config

class WarcraftAI:
    def __init__(self):
        self.loop = True
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
        


    def Start(self):
        try:
            self.MainLoop()
        except(KeyboardInterrupt):
            self.Stop()
            exit

    def Stop(self):
        print("Exiting...")
        self.loop = False
        self.socket.close()

    def match_templates(self,play_area):
        img_gray = cv2.cvtColor(play_area, cv2.COLOR_BGR2GRAY)

        units = [
                Unit(1,'./imgs/footman',(255,0,0),0.85,1),
                Unit(1,'./imgs/peasant',(0,100,255),0.85,0),
                Unit(1,'./imgs/buildings',(0,255,255),0.76,2),
                Unit(2,'./imgs/tree',(19,69,139),0.8,1),
                Unit(1,'./imgs/road',(255,255,255),0.8,2)
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
                            if(unit.mapmode == 2 and unit.location == './imgs/buildings'):
                                try:
                                    self.map[unit.mapmode][self.offset[0]+math.ceil(pt[1] / 16)][self.offset[1]+math.ceil(pt[0] / 16)] = int(filename[:len(filename)-4])
                                except:
                                    pass
                            else:
                                try:
                                    self.map[unit.mapmode][self.offset[0]+math.ceil(pt[1] / 16)][self.offset[1]+math.ceil(pt[0] / 16)] = unit.id
                                except:
                                    pass
                        cv2.rectangle(play_area, pt, (pt[0] + w, pt[1] + h), unit.color, 2)
                        cv2.imwrite('res.png',play_area)
                    

        

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
                    self.map[2][i][j] = -1
                elif(list(cropMap[i][j]) == [0,0,255]):
                    self.map[2][i][j] = 100
                elif(i+1 != 64 and j+1 != 64 and list(cropMap[i][j]) == [199,199,199] and list(cropMap[i+1][j]) == [199,199,199] and list(cropMap[i+1][j+1]) == [199,199,199] and  list(cropMap[i][j+1]) == [199,199,199]):
                    self.map[0][i][j] = 3
        
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
                elif(self.map[0][i][j] == 3):
                    mines.append([i,j])

        i = random.randint(1,2)
        for peasant in peasants:
            
            if(i % 2 == 0):
                if( len(trees) > 0):
                    self.commands.append(f"Gather {self.GetClickCoord(peasant[0],peasant[1],1)} { self.GetClickCoord(trees[0][0],trees[0][1],0)}")
                else:
                    self.MoveUnitUnexplored(peasant[0],peasant[1])
            else:
                if( len(mines) > 0):
                    self.commands.append(f"Gather {self.GetClickCoord(peasant[0],peasant[1],1)} { self.ClickOnMinimap(mines[0][1],mines[0][0])}")
                else:
                    self.MoveUnitUnexplored(peasant[0],peasant[1])
            i += 1

    def ExplorePhase(self):

        soldiers=[]
        target = None
        
        for i in range(64):
            for j in range(64):
                if(self.map[1][i][j] == 1):
                    soldiers.append([i,j])
        if(len(soldiers) > 0):
            self.MoveUnitUnexplored(soldiers[0][0]+1,soldiers[0][1]+0)


    def MoveUnitUnexplored(self,x,y):
        exitfor = False
        if(self.offset != None):
            for i in range(self.offset[0],self.offset[0]+15):        
                if exitfor:
                    break
                for j in range(self.offset[1],self.offset[1]+11):                    
                    if(self.map[1][i][j] == -1):          
                        target = [i,j]
                        if (random.randint(0,165) == 1):
                            exitfor = True
                            break
            print(f"a: {target}")
            self.commands.append(f"Move {self.GetClickCoord(x,y,1)} { self.ClickOnMinimap(target[0],target[1]) }")

    def BuildPhase(self):
        # 300 500
        # 500 600

        peasants = []
        locations = []

        for i in range(64):
            for j in range(64):
                if(self.map[0][i][j] == 1):
                    peasants.append([i,j])
                if(i < 62 and j < 62 and self.map[1][i][j] == 0 and self.map[1][i+1][j] == 0 and self.map[1][i][j+1] == 0 and self.map[1][i+1][j+1] == 0 ):
                    print(f"jó: {[j,i]}")
                    
                    road = False
                    building = False

                    for x in range(4):
                        if(self.map[2][j-1][i-1-(x)] == 1):
                            road = True
                            break

                    for x in range(4):
                        if(self.map[2][j-1+(x)][i-1] == 1):
                            road = True
                            break

                    for x in range(4):
                        if(self.map[2][j+2][i+1-(x)] == 1):
                            road = True
                            break

                    for x in range(4):
                        if(self.map[2][j-2+(x)][i-1] == 1):
                            road = True
                            break


                    for x in range(5):
                        if(self.map[2][j-2][i-2-(x)] == 1):
                            building = True
                            break

                    for x in range(5):
                        if(self.map[2][j-2+(x)][i-2] == 1):
                            building = True
                            break    

                    for x in range(5):
                        if(self.map[2][j+3][i+2-(x)] == 1):
                            building = True
                            break

                    for x in range(5):
                        if(self.map[2][j-3+(x)][i-2] == 1):
                            building = True
                            break

                    if(road and building):
                        locations.append([j,i])
           
        print(len(locations))
        if(len(locations) > 0):
            for peasant in peasants:
                    print(locations[0])
                    self.commands.append(f"Build {self.GetClickCoord(peasant[0],peasant[1],1)} 50 130 {self.GetClickCoord(locations[0][1],locations[0][0],0)}")


    def TrainPhase(self):
        for i in range(64):
            for j in range(64):
                if(self.map[2][i][j] == 1):
                    print([i,j])
                    self.commands.append(f"Click {self.GetClickCoord(i,j,-1)}")
                    self.commands.append(f"Click 30 120")
                    return


    def CombatPhase(self):
        for i in range(64):
            for j in range(64):
                if(self.map[2][i][j] == 100):
                    self.commands.append(f"Click {self.ClickOnMinimap(i,j)}")

    def GetClickCoord(self,x,y,z):
        x -= self.offset[0]+z
        y -= self.offset[1]+z

        return f"{160+y*32} {20+x*16}"

    def ClickOnMinimap(self,x,y):
        return (f"{2*x+6} {y+6}")

    def NextStage(self):
        self.stage += 1
        if self.stage > 5:
            self.stage = 0  

    def getValidLocations(self,cropmap):
        locations = []

        for i in range(64):
            for j in range(64):
                found = False
                if list(cropmap[i][j]) == [0,199,0]:                
                    for location in locations:
                        if ( (location[0] + 6 > j or location[1] + 6 > i) or (location[0] - 6 > j or location[1] - 6 > i)):
                            found = True
                            break
                    if not found:
                        locations.append([i,j])


        print(f"locations: {locations}")


    def MainLoop(self):
        time.sleep(5)
        self.socket.send(bytes("Start",'utf-8'))
        message = self.socket.recv()
        print(f"Received reply {message}")
        time.sleep(1)
        while self.loop:
            
            pytesseract.pytesseract.tesseract_cmd = Config.tesseract # Need to be dynamic

            image = cv2.imread(Config.capture)
            
            try:
                self.ReadText("Lumber",image[1:8,143:169])
                self.ReadText("Gold",image[1:8,243:269])       
                cv2.imwrite("map.png",image[6:70,3:67]) # térkép
                cv2.imwrite("playArea.png",image[12:188,72:312]) #játéktér

            except TypeError:
                continue

            
            self.UpdateMap(image[6:70,3:67])
            self.match_templates(image[12:188,72:312])
            self.getValidLocations(image[6:70,3:67])
            if(self.stage == 0):           
                pass
                self.GatherPhase()
            elif(self.stage == 1):
                pass
                self.ExplorePhase()
            elif(self.stage == 2):
                pass
                self.TrainPhase()
            elif(self.stage == 3):
                self.BuildPhase()
            elif(self.stage == 4):
                pass
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
            self.map[0] = np.zeros(shape=(64,64))
            self.map[2] = np.zeros(shape=(64,64))
            
            #cv2.waitKey()
            time.sleep(1)

class Unit:
    def __init__(self,unit_id,location,color,threshold,mapmode):
        self.location = location
        self.color = color
        self.threshold = threshold
        self.mapmode = mapmode
        self.unit_id = unit_id