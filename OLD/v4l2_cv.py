#!/usr/bin/env python

import numpy as np
import cv2
import os
import v4l2capture
import select
import imutils

if __name__ == '__main__':
    #cap = cv2.VideoCapture(0)
    #cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)      # <-- this doesn't work. OpenCV tries to set VIDIO_S_CROP instead of the frame format
    #cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
    
    
    # Open the video device.
    video = v4l2capture.Video_device("/dev/video1")
    video1 = v4l2capture.Video_device("/dev/video2")

    video.set_fps(30);
    video1.set_fps(30);

    #video.set_exposure_auto(1)
    number1 = video1.get_exposure_absolute()

    #print(number1)
    #video2 = v4l2capture.Video_device("/dev/video3")
    #video3 = v4l2capture.Video_device("/dev/video4")

    size_x, size_y = video.set_format(480, 640, fourcc='MJPG')
    size_x, size_y = video1.set_format(480, 640, fourcc='MJPG')
    #size_x, size_y = video2.set_format(1280, 720, fourcc='MJPG')
    #size_x, size_y = video3.set_format(1280, 720, fourcc='MJPG')
    
    print "device chose {0}x{1} res".format(size_x, size_y)
    
    # Create a buffer to store image data in. This must be done before
    # calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
    # raises IOError.
    video.create_buffers(30)
    video1.create_buffers(30)
    #video2.create_buffers(30)
    #video3.create_buffers(30)
    
    # Send the buffer to the device. Some devices require this to be done
    # before calling 'start'.
    video.queue_all_buffers()
    video1.queue_all_buffers()
    #video2.queue_all_buffers()
    #video3.queue_all_buffers()
    
    # Start the device. This lights the LED if it's a camera that has one.
    print "start capture"
    video.start()
    video1.start()
    #video2.start()
    #video3.start()

    while(True):
        #We used to do the following, but it doesn't work :(
        #ret, frame = cap.read()
        
        #Instead...
        
        # Wait for the device to fill the buffer.
        print(number1)
        select.select((video,), (), ())
        select.select((video1,), (), ())
        #select.select((video2,), (), ())
        #select.select((video3,), (), ())

        # The rest is easy :-)
        image_data = video.read_and_queue()
        image_data1 = video1.read_and_queue()
        #image_data2 = video2.read_and_queue()
        #image_data3 = video3.read_and_queue()
        
        print "decode"
        frame = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), 1)
        frame1 = cv2.imdecode(np.frombuffer(image_data1, dtype=np.uint8), 1)
        #frame2 = cv2.imdecode(np.frombuffer(image_data2, dtype=np.uint8), 1)
        #frame3 = cv2.imdecode(np.frombuffer(image_data3, dtype=np.uint8), 1)
    	num_rows, num_cols = frame.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), 90, 1)
        img_rotation = cv2.warpAffine(frame, rotation_matrix, (num_cols, num_rows))

        cv2.namedWindow("frame0")
        cv2.namedWindow("frame1")
        #cv2.namedWindow("frame2")
        #cv2.namedWindow("frame3")
        cv2.imshow('frame0', img_rotation)

        cv2.imshow('frame1', frame1)
        #cv2.imshow('frame2', frame2)
        #cv2.imshow('frame3', frame3)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            break

    #cap.release()
    video.close()
    video1.close()
    #video2.close()
    #video3.close()
    
    cv2.destroyAllWindows()