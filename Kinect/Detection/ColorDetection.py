from BasicFunctions import *

image_hsv = [None,None,None]
pixel = (20,60,80)
name = 0    #red = 0 green = 1 blue = 2
next_name = None
pressed = 1


lowers = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
uppers = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

first_run = True


def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[name][y,x]

        #you might want to adjust the ranges(+-10, etc):
        lm = 60
        upper =  np.array([pixel[0] + lm, pixel[1] + lm, pixel[2] + lm])
        lower =  np.array([pixel[0] - lm, pixel[1] - lm, pixel[2] - lm])
        lowers[name] = [lower[0],lower[1],lower[2]]
        uppers[name] = [upper[0],upper[1],upper[2]]

        image_mask = cv2.inRange(image_hsv[name],lower,upper)
        new_name = str(name).replace('0', 'red').replace('1', 'green').replace('2', 'blue')
        cv2.imshow(new_name,image_mask)

def calibrate_color(name_, use_frame = False, frame=None):
    global name
    name = name_
    global image_hsv, pixel, mouse # so we can use it in mouse callback

    if use_frame and not frame is None:
        image_src = frame
    else:
        image_src = get_video()
    if image_src is None:
        print ("the image read is None............")
        return

    ## NEW ##
    new_name = name_

    cv2.namedWindow('hsv for ' + str(new_name))
    cv2.setMouseCallback('hsv for ' + str(new_name), pick_color)

    # now click into the hsv img , and look at values:
    image_hsv[name] = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv for " + str(new_name), image_hsv[name])
    cv2.waitKey(0)

def calibrate_colors(onlyone = True, col=0, use_frame = False, frame = None):
    if onlyone:
        calibrate_color(col)
    elif use_frame and not frame is None:
        calibrate_color(0, use_frame, frame)
        calibrate_color(1, use_frame, frame)
        calibrate_color(2, use_frame, frame)
    else:
        calibrate_color(0)
        calibrate_color(1)
        calibrate_color(2)
    cv2.destroyWindow("hsv for 0")
    cv2.destroyWindow("hsv for 1")
    cv2.destroyWindow("hsv for 2")
    cv2.destroyWindow("red")
    cv2.destroyWindow("green")
    cv2.destroyWindow("blue")

prevc = []

def drawDetectColors(name, frame, color, colorName="Bottle", use_frame=False, c=(0,0,0)):
    global first_run, prevc

    if first_run or not c in prevc:
        calibrate_colors(col = int(color), onlyone = True, use_frame=use_frame, frame=frame)
        first_run = False
        prevc.append(c)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    global lowers, uppers

    id = int(color)
    lower = np.array([lowers[id][0],lowers[id][1],lowers[id][2]])
    upper = np.array([uppers[id][0],uppers[id][1],uppers[id][2]])
    mask = cv2.inRange(hsv, lower, upper)

    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    center = []
    for cnt in contours:
        if cv2.contourArea(cnt) > 300:
            # print(cv2.contourArea(cnt))
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            center = [cX,cY]
            cv2.circle(frame, (cX, cY), 3,c,2)
            cv2.putText(frame,colorName,(cX, cY), cv2.FONT_HERSHEY_PLAIN, 1,c,2,cv2.LINE_AA)
            center = [[cX, cY], colorName]
            # cv2.drawContours(frame, [cnt], 0, c, 3)
            break
    cv2.imshow(name,frame)
    return center