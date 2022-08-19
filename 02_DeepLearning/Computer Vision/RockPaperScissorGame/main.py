# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#https://github.com/cvzone/cvzone/blob/master/cvzone/HandTrackingModule.py
#https://medium.com/analytics-vidhya/mediapipe-fingers-counting-in-python-w-o-gpu-f9494439090c
#https://google.github.io/mediapipe/solutions/hands.html#multi_handedness

import cv2
import mediapipe as mp
import time

class handDetector():
    def __init__(self, mode= False, maxHands=1, detectionCon=0.8, trackCon = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode = self.mode ,max_num_hands = self.maxHands,min_detection_confidence=self.detectionCon,min_tracking_confidence=self.trackCon)
        #self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        label=" "
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self , img, handNO =0, draw = True):

            lmList = []
            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNO]
                for id, lm in enumerate(myHand.landmark):
                    #print(id, lm)
                    h,w,c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    #print(id, lm)
                    lmList.append([id,cx,cy])
                    #if id ==4 :
                        #print("Filled")
                    if draw:
                        cv2.circle(img, (cx,cy), 5,(255,0,255), cv2.FILLED)

            return lmList



    def getFingers(self, lmList, hndtype):

        lstfingures = [] #[thumb, index fingure, middle fingure, Ring Fingure, Little Fingure]
        if len(lmList)!=0:
            #thumb
            if (hndtype == "Right" and (lmList[4][1] > lmList[3][1])) or \
            (hndtype == "Left" and (lmList[4][1] < lmList[3][1])):
                lstfingures.append(1)
            else:
                lstfingures.append(0)

            #Middle  finger
            if lmList[8][2] < lmList[6][2]:
                lstfingures.append(1)
            else:
                 lstfingures.append(0)

            #Middle  finger
            if lmList[12][2] < lmList[10][2]:
                lstfingures.append(1)
            else:
                 lstfingures.append(0)

            #Ring  finger
            if lmList[16][2] < lmList[14][2]:
                lstfingures.append(1)
            else:
                 lstfingures.append(0)

            #Little  finger
            if lmList[20][2] < lmList[18][2]:
                lstfingures.append(1)
            else:
                 lstfingures.append(0)



        return lstfingures

    def getHandType(self,handNO=0):
        type = " "
        if self.results.multi_handedness:
            type = self.results.multi_handedness[handNO].classification[0].label
               #account for inversion in webcams
            if type == "Left":
                type = "Right"
            elif type == "Right":
                type = "Left"

        return type

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def main():

    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()


    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        label = detector.getHandType(0)
        fingures = detector.getFingers(lmList=lmList, hndtype=label)
        print("Hand Type = ",fingures)
        if len(lmList) !=0:
            print(lmList[4])
        cTime = time.time()
        fps =  1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3  )


        cv2.imshow("image", img)
        cv2.waitKey(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

