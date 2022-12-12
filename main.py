import cv2
import numpy as np
import utils


webcam = False
path = '1.jpg'
cap = cv2.VideoCapture(0)
cap.set(10, 160)
cap.set(3, 1920) #1920
cap.set(4, 1080) #1080
scale = 3
wP = 190 * scale
hP = 297 * scale


while True:
    if webcam:
        success, img = cap.read()
    else:
        img = cv2.imread(path)

    img, conts = utils.getContours(img, minArea=50000, filter=4, showCanny=False)
    if len(conts) != 0:
        biggest = conts[0][2]
        imgWarp = utils.warpImg(img, biggest, wP, hP)
        cv2.imshow('A4 Paper', imgWarp)

        img2, conts2 = utils.getContours(imgWarp, minArea=2000, filter=4, cThr=[50,50], draw=True)
        cv2.imshow('A4 Paper', img2)

        if len(conts2) != 0:
            for obj in conts2:
                cv2.polylines(img2, [obj[2]], True, (255, 0, 0), 5)
                npoints = utils.reorder((obj[2]))
                # print(npoints)
                nw = round((utils.findDis(npoints[0][0]//scale, npoints[1][0]//scale)/10), 1)
                nh = round((utils.findDis(npoints[0][0]//scale, npoints[2][0]//scale)/10), 1)
                Nw = str(nw)+'cm'
                Nh = str(nh)+'cm'
                # print(type(Nw))
                # print(type(Nh))
                print('Width: ', nw, 'Height: ', nh)

                cv2.arrowedLine(img2, (npoints[0][0][0], npoints[0][0][1]), (npoints[1][0][0], npoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(img2, (npoints[0][0][0], npoints[0][0][1]), (npoints[2][0][0], npoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = obj[3]
                # print('x=', x, 'y=', y, 'w=', w, 'h=', h)
                cv2.putText(img2, '{}cm'.format(nw), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
                cv2.putText(img2, '{}cm'.format(nh), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)

    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    # img = cv2.resize(img, (1050, 1610))
    cv2.imshow('Original', img)
    cv2.waitKey(1)
