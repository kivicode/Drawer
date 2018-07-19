from BasicFunctions import *
# from Drawing.ParseArduino import eval
import cv2
import cv2.aruco as aruco
import main
font = cv2.FONT_HERSHEY_PLAIN


def drawMarkers(name, frame, calibrateByMarker = False, dist = 0):
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
         
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    (h, w) = frame.shape[:2]
    detect = aruco.drawDetectedMarkers(frame, corners)
    

    if len(corners) >= 1:
        rect = cv2.boxPoints(cv2.minAreaRect(corners[0]))
        cv2.drawContours(frame,[np.int0(rect)],-1,(0,0,255),3)
        id_count = 0;
        current = np.int0(rect)
        midx = 0
        midy = 0
        for pos in current:
            midx += pos[0]
            midy += pos[1]
            cv2.circle(frame,(pos[0], pos[1]),3,(255,255,0),2)
        midx /= len(current)
        midy /= len(current)
        dist = int(getDist(midx,midy))+20
        angle = getAngleFromDepth(midx, midy, dist, w)
        dY = math.tan(math.radians(angle))*int(dist)
        ndY = map(dY, -407, 407, 0, 2000)
        print(ids[id_count][0])
        cv2.circle(frame,(int(midx), int(midy)),3,(255,0,255),2)
            #print(dist, angle, dY)
        if calibrateByMarker and ids[id_count][0] == 4:
            print("Marker found")
            angle = getAngleFromDepth(midx, midy, dist, w)
            #angle = map(angle, -20, 20, -25, 25)
            side = "right"
            if angle < 0:
                side = "left"
            eval(side+"("+str(abs(angle))+");")
            eval("f("+str(dist*0.67)+");")
            #      print("Boolean =", main.calibrateByMarker, "Id =", ids[id_count][0])
        n = str(ids[id_count][0])
        midx -= (len(n)-1)*10
        midy += 10
        cv2.putText(frame,n,(int(midx),int(midy)), font, 3,(255,255,255),2,cv2.LINE_AA)
        id_count += 1
    cv2.imshow(name,detect)



def getName(id):
    name = ''

    if id == 1:
        name = 'A'
    elif id == 2:
        neme = 'B'
    elif id == 3:
        neme = 'C'
    elif id == 4:
        neme = 'D'
    elif id == 5:
        neme = 'E'
    elif id == 6:
        neme = 'F'
    elif id == 7:
        neme = 'G'
    elif id == 8:
        neme = 'H'
    elif id == 9:
        neme = 'I'
        return name