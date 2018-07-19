commands = []

from Detection.DepthDetection import *
from Detection.MarkerDetection import *
from Detection.QRCodeDetection import *
from Detection.BarcodeDetection import *
from Detection.ColorDetection import *
from Detection.ObjectDetection import *
from Detection.ContourDetection import *
# from Drawing.DrawWay import *
# from Drawing.ParseArduino import eval
# from Drawing.FollowWay import *
# from Tests.test import *
from BasicFunctions import *
import cv2
depth = False
marker = False
qrcode = False
bottles = False
objects = False
test = False
colors = True
# main.calibrateByMarker = False

globalName = "Depth"

distToObject = 0

path = ["f(900)", "r(90)", "f(400)"]
fr = True


    
if __name__ == "__main__":
    # writeToFile("Commands.txt", "", clear=True)
    # frame = get_video()
    cv2.namedWindow(globalName, cv2.WND_PROP_FULLSCREEN)

    #follow(path)
    while 1:
        frame = getCamVideo()#get_video()
        detectContours(globalName+"1",getCamVideo())
    

        # dm = getDepthMap()
        #getBrightest(dm, 100)
        #cv2.circle(frame, minLoc, 5, 3,(0,255,0),2)
        # print(camFrame)
        # cv2.imshow("Monipulator Cam", frame)

        if depth:
            drawContours(globalName, frame, 500, False)

        if marker:
            newDist = float(main.distToObject) * 0.33
            drawMarkers(globalName, frame, calibrateByMarker =False, dist = newDist)
            # print(main.calibrateByMarker)
            main.calibrateByMarker = False
        if qrcode:
            drawDecodedQRcode(globalName, frame)

        if bottles:
            drawObjects(globalName, frame, filter="bottle", return_bottle_imgs = True)

        if objects:
            drawObjects(globalName, frame)

        if colors:
            pulpy = drawDetectColors(globalName, frame, 0, colorName="Pulpy", c=(0,0,255))
            # lipton = drawDetectColors(globalName, frame, 1, colorName="Lipton", c=(0,255,0))
            # followPoint(pulpy[0])
            # if fr and pulpy[0] != [0,0]:
            #     followPoint(pulpy[0])
            #     fr = False
            # drawDetectColors(globalName, frame, 1, c=(0,255,0))
            # drawDetectColors(globalName, frame, 2, c=(255,0,0))

        if test:
            surfDetection(globalName, frame)

 
        k = cv2.waitKey(5) & 0xFF
        if k == ord('q'):
            break
        elif k == ord('d'):
            depth = (not depth)
        elif k == ord('m'):
            marker = (not marker)
        elif k == ord('n'):
            qrcode = (not qrcode)
        elif k == ord('b'):
            bottles = (not bottles)
        elif k == ord('o'):
            objects = (not objects)
        elif k == ord('p'):
            calibrateByMarker = not calibrateByMarker
        elif k == ord('r'):
            reset()
        elif k == ord('g'):
            goHome();
    cv2.destroyAllWindows()