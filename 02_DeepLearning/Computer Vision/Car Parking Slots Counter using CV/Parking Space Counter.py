import cv2
import pickle
import numpy as np

Vfeed = cv2.VideoCapture("Resources/carPark.mp4")
with open("parking_positions.pk1", 'rb') as f:
    parking_pos_list = pickle.load(f)

def checkParkingSpace(imgPro):
    spaceCounter = 0
    availableSpace = []
    for pos in parking_pos_list:
        print(pos)
        x,y, parkingNum = pos[0], pos[1], pos[2]
        print(x,y, parkingNum)
        if x[0] >0:
        #imgCrop = imgPro[y:y + height, x:x + width]
            imgCrop = imgPro[x[1]:y[1],x[0]:y[0]]
            try:
                #cv2.imshow(str(x[0] * y[1]), imgCrop)
                count = cv2.countNonZero(imgCrop)
                print(count)
                if count < 1000:
                    color = (0, 255, 0)
                    thickness = 2
                    spaceCounter += 1
                    availableSpace.append(parkingNum)
                else:
                    color = (0, 0, 255)
                    thickness = 2
                #cv2.rectangle(img, x,y, color, thickness)
                c1, c2 = int((x[0]+y[0])/2), int((x[1]+y[1])/2)

                colorTxt = (255, 0, 0)
                #cv2.putText(img, str(parkingNum), org, cv2.FONT_HERSHEY_SIMPLEX,1,colorTxt, 1)
                #print("center - ", org)
                w, l = 15, 10
                if parkingNum > 9:
                    org = (c1-10,c2+5)
                else:
                    org = (c1-5,c2+5)

                laneA, laneB,laneC = "","",""
                availableSpace.sort()
                #print("availableSpace")
                #print(availableSpace)
                for sp in availableSpace:
                    #print(sp)
                    if sp <=22 :
                        laneA = laneA +"," +str(sp)
                    elif (sp >= 23 and sp <=42) :
                        laneB = laneB + "," +str(sp)
                    else:
                        laneC = laneC +","+str(sp)

                laneA = laneA[1:]
                laneB = laneB[1:]
                laneC = laneC[1:]
                cv2.rectangle(img, ((c1-w),(c2-l)) ,((c1+w),(c2+l)), color, -1)
                cv2.putText(img, str(parkingNum),org,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,128,0))


                print("lanea - ",laneA)
            except:
                print("cannot load image - ", x,y)
    lanetextcolor = (204,232,19)
    lanefontscale = 1.0
    lanefont = 1
    lanefontthickness= 2
    lanelinetype =  cv2.FILLED
    cv2.rectangle(img, (64,42) ,(245,77), color, 1)
    cv2.rectangle(img, (411,42) ,(592,77), color, 1)
    cv2.rectangle(img, (766,42) ,(1000,77), color, 1)

    cv2.putText(img, "Free Parking Slots ", (64,40),lanefont,lanefontscale, (78,89,70),1,1)
    cv2.putText(img, "Free Parking Slots ", (411,40),lanefont,lanefontscale, (78,89,70),1,1)
    cv2.putText(img, "Free Parking Slots", (766,40),lanefont,lanefontscale, (78,89,70),1,1)

    cv2.putText(img, (laneA),(77,60),lanefont, lanefontscale, lanetextcolor,lanefontthickness,lanelinetype)
    cv2.putText(img, (laneB),(420,60),lanefont, lanefontscale, lanetextcolor,lanefontthickness,lanelinetype)
    cv2.putText(img, (laneC),(770,60),lanefont, lanefontscale, lanetextcolor,lanefontthickness,lanelinetype)

    cv2.putText(img, "Total Free Slots - "+str(spaceCounter)+"/63",(30,15),lanefont, lanefontscale, lanetextcolor,1,1)

    laneA, laneB,laneC = "","",""




while True:
    if Vfeed.get(cv2.CAP_PROP_POS_FRAMES) == Vfeed.get(cv2.CAP_PROP_FRAME_COUNT):
        Vfeed.set(cv2.CAP_PROP_POS_FRAMES,0)
    success, img = Vfeed.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
    checkParkingSpace(imgDilate)
    #cv2.imshow("Parking Area", imgDilate)
    #for vertex in parking_pos_list:
    #    pt1 = vertex[0]
    #    pt2 = vertex[1]
        #cv2.rectangle(parking_area, (pt1,pt2),(pt1+length,pt2+width),(255, 0, 255), 2)
        #cv2.rectangle(img,pt1, pt2 ,(255, 0, 255), 2)

    cv2.imshow("Parking Area1", img)
    cv2.waitKey(10)

