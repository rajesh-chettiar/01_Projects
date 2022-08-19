import random

from HandDetectionModule import handDetector
import cvzone
import cv2
import mediapipe as mp
import time



detector = handDetector()
cap = cv2.VideoCapture(0)
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]
playerMoveLabel = None
while True:

        path = "Resources/"
        bgImage = cv2.imread(path+"BG.png")
        success, img = cap.read()
        resizeImg = cv2.resize(img,(0,0), None, 0.875,0.875)
        resizeImg = resizeImg[:,80:480]

        img = detector.findHands(resizeImg)
        lmList = detector.findPosition(resizeImg)

        if startGame:
                if stateResult is False:
                        timer = time.time() - initialTime
                        cv2.putText(bgImage, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
                        cv2.putText(imgBG, str(playerMoveLabel), (846, 611), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
                if timer > 3:
                        stateResult = True
                        timer = 0
                        playerMove = None
                        playerMoveLabel = None
                        if len(lmList)!=0:
                                playerMove = None
                                playerMoveLabel = None
                                #hand = hands[0]
                                label = detector.getHandType(0)
                                fingers = detector.getFingers(lmList=lmList, hndtype=label)

                                if fingers == [0, 0, 0, 0, 0]:
                                        playerMove = 1
                                        playerMoveLabel = "Rock"
                                if fingers == [1, 1, 1, 1, 1]:
                                        playerMove = 2
                                        playerMoveLabel = "Paper"
                                if fingers == [0, 1, 1, 0, 0]:
                                        playerMove = 3
                                        playerMoveLabel = "Scissor"


                                #AI Graphics
                                rand =  random.randint(1,3)
                                AiMove = cv2.imread(path+str(rand)+".png", cv2.IMREAD_UNCHANGED)
                                bgImage = cvzone.overlayPNG(bgImage, AiMove, (149, 310))

                                #print("Hand Type = ",fingers)

                                # Player Wins
                                if (playerMove == 1 and rand == 3) or \
                                            (playerMove == 2 and rand == 1) or \
                                            (playerMove == 3 and rand == 2):
                                        scores[1] += 1

                                # AI Wins
                                if (playerMove == 3 and rand == 1) or \
                                            (playerMove == 1 and rand == 2) or \
                                            (playerMove == 2 and rand == 3):
                                        scores[0] += 1

        bgImage[234:654,795:1195] = resizeImg
        imgBG =bgImage
        if stateResult:
                imgBG = cvzone.overlayPNG(bgImage, AiMove, (149, 310))

        cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(imgBG, str(playerMoveLabel), (846, 611), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

        cv2.imshow("game", imgBG)
        key = cv2.waitKey(1)
        if key == ord('s'):
                startGame = True
                initialTime = time.time()
                stateResult = False
                playerMoveLabel = ""
        #cv2.imshow("", img)

