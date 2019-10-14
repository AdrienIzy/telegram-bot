
import cv2
import numpy as np
from threading import Timer
from time import sleep as sl

isOn = [True]

def capt(duree, camInd):
    print("Capturing...")
    isOn[0] = True
    if(duree>0 and duree<=11):
        cap = cv2.VideoCapture(camInd)
        for i in range(50):
            cap.read()
            sl(0.01)
        t = Timer(duree+1.5, setOff, args=None, kwargs=None)
        t.start()
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
     
        out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height))
     
        while(isOn[0] == True):
          ret, frame = cap.read()
     
          if ret == True: 
         
            out.write(frame)
            #cv2.imshow('frame',frame)
     
            if cv2.waitKey(1) & 0xFF == ord('q'):
              break
     
          else:
            break 
 
        cap.release()
        out.release()
        #cv2.destroyAllWindows()
        print("...end of capture")
        return (frame_width,frame_height,duree)
    elif(duree == 0):
        cap = cv2.VideoCapture(camInd)
        for i in range(30):
            cap.read()
            sl(0.01)
        check, frame = cap.read()
        cv2.imwrite('capture'+str(camInd)+'.jpg', frame)
        print("...end of capture")
        return (0,0,0)

def setOff():
    isOn[0] = False

def multicapt(duree):
    print("Capturing...")
    isOn[0] = True
    ind = [0, 0, 0]
    caps = []
    outs = []
    duree = duree*len(ind)
    for i in range(len(ind)):
        caps.append(cv2.VideoCapture(ind[i]))
    frame_width = int(caps[0].get(3))
    frame_height = int(caps[0].get(4))
    for i in range(len(ind)):
        outs.append(cv2.VideoWriter('outpy'+str(i)+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 30, (frame_width,frame_height)))
    if(duree>0 and duree<=11):
        for i in range(50):
            for j in range(len(ind)):
                caps[j].read()
            sl(0.01)
        t = Timer(duree+1.5, setOff, args=None, kwargs=None)
        t.start()
        while(isOn[0] == True):
            for i in range(len(ind)):
              ret, frame = caps[i].read()
              if ret == True: 
                outs[i].write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                  break
              else:
                break
        for i in range(len(ind)):
            caps[i].release()
            outs[i].release()
        #cv2.destroyAllWindows()
        print("...end of capture")
        return (len(ind))
    else:
        capt(duree,0)
        capt(duree,1)
        capt(duree,2)
        return 3
        
#capt(0,0)
#capt(3,1)
#multicapt(2)
