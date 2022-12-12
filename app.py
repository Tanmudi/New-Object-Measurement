import streamlit as st
import cv2
import numpy as np
import utils
from PIL import Image


scale = 3
wP = 190 * scale
hP = 297 * scale

st.sidebar.title('Sidebar')

pages = st.sidebar.radio("Navigation",["Home", "About Us"])

if pages=='Home':
    st.title('Object Measurement')
    options = st.radio("Options", ["Measure in Image", "Measure in Live feed"])

    if options=="Measure in Image":
        st.header('Image Input')

        img_input = st.file_uploader("Upload a file")

        if img_input:
            st.image(img_input)

            img = np.array(Image.open(img_input))

            img, conts = utils.getContours(img, minArea=50000, filter=4, showCanny=False)

            if len(conts) != 0:
                biggest = conts[0][2]
                imgWarp = utils.warpImg(img, biggest, wP, hP)

                img2, conts2 = utils.getContours(imgWarp, minArea=2000, filter=4, cThr=[50,50], draw=False)

                st.subheader("Output Image")

                if len(conts2) != 0:
                    for obj in conts2:
                        cv2.polylines(img2, [obj[2]], True, (0, 255, 0), 5)
                        npoints = utils.reorder((obj[2]))
                        nw = round((utils.findDis(npoints[0][0]//scale, npoints[1][0]//scale)/10), 1)
                        nh = round((utils.findDis(npoints[0][0]//scale, npoints[2][0]//scale)/10), 1)

                        cv2.arrowedLine(img2, (npoints[0][0][0], npoints[0][0][1]), (npoints[1][0][0], npoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                        cv2.arrowedLine(img2, (npoints[0][0][0], npoints[0][0][1]), (npoints[2][0][0], npoints[2][0][1]),
                                        (255, 0, 255), 3, 8, 0, 0.05)
                        x, y, w, h = obj[3]
                        cv2.putText(img2, '{}cm'.format(nw), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                    (255, 0, 255), 2)
                        cv2.putText(img2, '{}cm'.format(nh), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                    (255, 0, 255), 2)
                st.image(img2)


    
    if options=="Measure in Live feed":
        st.header('Live Video capture')

        use_webcam = st.button('Use Webcam')

        if use_webcam:
            stframe=st.empty()
            stframe2=st.empty()
            vid = cv2.VideoCapture(1)
            
            width=int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            height=int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps_input=int(vid.get(cv2.CAP_PROP_FPS))

            codec = cv2.VideoWriter_fourcc('M','J','P','G')
            out_input = cv2.VideoWriter('Input.mp4', codec, fps_input, (width, height))
            out_output = cv2.VideoWriter('Output.mp4', codec, fps_input, (width, height))

            while vid.isOpened():
                
                success, img = vid.read()

                out_input.write(img)

                img_out = cv2.resize(img, (0, 0), None, 0.5, 0.5)
                stframe.image(img_out, channels='BGR', use_column_width=True)

                img, conts = utils.getContours(img, minArea=50000, filter=4, showCanny=False)

                if len(conts) != 0:
                    biggest = conts[0][2]
                    imgWarp = utils.warpImg(img, biggest, wP, hP)

                    img2, conts2 = utils.getContours(imgWarp, minArea=2000, filter=4, cThr=[50,50], draw=False)
                    
                    # st.subheader("Output Image")

                    if len(conts2) != 0:
                        for obj in conts2:
                            cv2.polylines(img2, [obj[2]], True, (0, 255, 0), 5)
                            npoints = utils.reorder((obj[2]))
                            nw = round((utils.findDis(npoints[0][0]//scale, npoints[1][0]//scale)/10), 1)
                            nh = round((utils.findDis(npoints[0][0]//scale, npoints[2][0]//scale)/10), 1)

                            cv2.arrowedLine(img2, (npoints[0][0][0], npoints[0][0][1]), (npoints[1][0][0], npoints[1][0][1]),
                                    (255, 0, 255), 3, 8, 0, 0.05)
                            cv2.arrowedLine(img2, (npoints[0][0][0], npoints[0][0][1]), (npoints[2][0][0], npoints[2][0][1]),
                                            (255, 0, 255), 3, 8, 0, 0.05)
                            x, y, w, h = obj[3]
                            cv2.putText(img2, '{}cm'.format(nw), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                        (255, 0, 255), 2)
                            cv2.putText(img2, '{}cm'.format(nh), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                                        (255, 0, 255), 2)
                    # st.image(img2)
                    out_output.write(img2)
                    img2 = cv2.resize(img2, (0, 0), None, 0.5, 0.5)
                    stframe2.image(img2, channels='BGR', use_column_width=True)



if pages=='About Us':
    st.title('About Us')
    st.header('Project Description')
    st.markdown("""
    In this project, We are getting the dimensions of the object using openCV.<br> Here, you have to keep a white paper as a background and
    then keep the rectangular object on that white paper to get its measurement. You can do it in realtime or also upload a photo to do so.
    """, True)
    st.header('Group Details')
    st.markdown("""
    **1. Tanmay Joshi**<br>
    **2. Omkar Pawar**<br>
    **3. Nayan Nirvikar**<br>
    **4. Sunil Lad**
    """, True)