import pickle
import cv2

counter = 0

with open("parking_positions.pk1", 'rb') as f:
    parking_pos_list = pickle.load(f)
temp = parking_pos_list
print(parking_pos_list)

#for pos in temp:

i=1
print(temp[0])
temp[i] = ((temp[i][0]), temp[i][1], (1))
print(temp[0])

def add_slots(event, x,y, flags, userdata):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        counter = counter + 1
        for i, pos in enumerate(parking_pos_list):
            if len(pos) <3:
                x1, y1 = pos
            else:
                 x1, y1, count1 = pos

            print(x1,y1)
            print(x,y)
            if x1[0] < x < y1[0] and x1[1] < y < y1[1]:

                parking_pos_list[i] = (parking_pos_list[i][0], parking_pos_list[i][1], counter)
                print("marked - ",str(counter))
                break;
    with open("parking_positions.pk1", 'wb') as f:
        pickle.dump(parking_pos_list, f)

while True:
     parking_area = cv2.imread("Resources/carParkImg.png")

     for vertex in parking_pos_list:
        pt1 = vertex[0]
        pt2 = vertex[1]
        #cv2.rectangle(parking_area, (pt1,pt2),(pt1+length,pt2+width),(255, 0, 255), 2)
        cv2.rectangle(parking_area,pt1, pt2 ,(255, 0, 255), 2)
     cv2.imshow("Parking Area", parking_area)
     cv2.setMouseCallback("Parking Area", add_slots)
     cv2.waitKey(1)



