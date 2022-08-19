import cv2
import pickle
length, width = 100,50
pt1, pt2 = 50,85


try:
    with open("parking_positions.pk1", 'rb') as f:
        parking_pos_list = pickle.load(f)
except:
    parking_pos_list = []

def draw_parking_area(event, x,y, flags, userdata):
    global ref_point, crop
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = (x,y)
    elif event == cv2.EVENT_LBUTTONUP:
        parking_pos_list.append((ref_point,(x,y)))
        cv2.rectangle(parking_area,ref_point, (x,y) ,(255, 0, 255), 2)

    if event == cv2.EVENT_RBUTTONDOWN:
         for i, pos in enumerate(parking_pos_list):
            x1, y1 = pos
            print(x1,y1)
            print(x,y)
            if x1[0] < x < y1[0] and x1[1] < y < y1[1]:

                parking_pos_list.pop(i)
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
    cv2.setMouseCallback("Parking Area", draw_parking_area)
    cv2.waitKey(1)



