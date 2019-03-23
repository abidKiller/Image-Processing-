import cv2
import numpy as np
from time import sleep




cap=cv2.VideoCapture(0)


lower = {'RED': (160, 86, 141), 'GREEN': (25, 189, 118),
         'BLUE': (97, 100, 117),'YELLOW': (20, 93, 20) }                           #


upper = {'RED': (186, 255, 255),'GREEN': (95, 255, 198),
         'BLUE': (117, 255, 255),'YELLOW': (30, 255, 255)
        }                                                  # '


colors = {'RED': (0, 0, 255), 'GREEN': (0, 255, 0), 'BLUE': (255, 0, 0),'YELLOW': (0, 255, 217),
          'ORANGE': (0, 140, 255)}




#input = ser.read()

while True:
    ret,real=cap.read()    

    kernel= np.ones((9,9),np.uint8)    

    blur=cv2.GaussianBlur(real,(9,9),0)

    hsv=cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)


    for key ,value in upper.items():

        mask = cv2.inRange(hsv,lower[key],upper[key])

        mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)

        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)

        contour,jddhv= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        length=len(contour)

        if length >0:

            maxcont=max(contour,key=cv2.contourArea)


            x,y,w,h=cv2.boundingRect(maxcont)

            M=cv2.moments(maxcont)

            center=(int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))

            if h>20 and w>20:

                cv2.rectangle(real,(x,y),(x+w,y+h),colors[key],2)

                font = cv2.FONT_HERSHEY_COMPLEX

            #    if key == 'RED':
             #       ser.write(b'1')

              #  elif key == 'BLUE':
               #     ser.write(b'2')

                #elif key == 'GREEN':
                #    ser.write(b'3') # GREEN
                #else :
                 #   ser.write(b'4') # YELLOW

                cv2.putText(real,key,center,font,2,colors[key],5,cv2.LINE_AA)

                print("detected color :: ", key)

                #sleep(2)

            cv2.imshow('mask', mask)
              # cv2.morphologyEx(real,)

    cv2.imshow('COLOR DETECTOR',real)



   # print('out')

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()