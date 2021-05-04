#!/usr/bin/env python
# -*- coding:utf-8 -*-
import argparse
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow_hub as hub
import numpy as np
import cv2
import time
import sys

if __name__ == '__main__':
    # parse options
    parser = argparse.ArgumentParser(description='han_cho_bot.')
    parser.add_argument('-d', '--device', default='normal_cam', help="normal_cam, jetson_nano_raspi_cam, raspi_cam")
    args = parser.parse_args()

    if args.device == 'normal_cam':
        cam = cv2.VideoCapture(0)
    elif args.device == 'jetson_nano_raspi_cam':
        GST_STR = 'nvarguscamerasrc \
            ! video/x-raw(memory:NVMM), width=1920, height=1080, format=(string)NV12, framerate=(fraction)30/1 \
            ! nvvidconv ! video/x-raw, width=(int)640, height=(int)480, format=(string)BGRx \
            ! videoconvert \
            ! appsink drop=true sync=false'
        cam = cv2.VideoCapture(GST_STR, cv2.CAP_GSTREAMER) # Raspi cam
    elif args.device == 'jetson_nano_web_cam':
        cam = cv2.VideoCapture(1)
    elif args.device == 'raspi_cam':
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        cam = PiCamera()
        cam.resolution = (640, 480)
        stream = PiRGBArray(cam)
    else:
        print('[Error] --device: wrong device')
        parser.print_help()
        sys.exit()

    labels = []
    with open('labels.txt', 'r') as f:
        for line in f:
            labels.append(line.rstrip())
    print(labels)

    model_pred = tf.keras.models.load_model('dice_model.h5', custom_objects={'KerasLayer':hub.KerasLayer})

    max_count = 0
    count = 0
    while True:
        if args.device == 'raspi_cam':
            cam.capture(stream, 'bgr', use_video_port=True)
            img = stream.array
        else:
            ret, img = cam.read()
            if not ret:
                print('error')
                break

        key = cv2.waitKey(1)
        if key == 27:  # when ESC key is pressed break
            break

        count += 1
        if count > max_count:
            X = []
            img_org = cv2.resize(img, (640, 480))
            img = cv2.resize(img, (256, 256))
            img = img_to_array(img)
            X.append(img)
            X = np.asarray(X)
            X = X/255.0
            start = time.time()
            preds = model_pred.predict(X)
            elapsed_time = time.time() - start

            pred_label = ''

            label_num = 0
            tmp_max_pred = 0
            print(preds)
            for i in preds[0]:
                if i > tmp_max_pred:
                    pred_label = labels[label_num]
                    tmp_max_pred = i
                label_num += 1

            # Put speed
            speed_info = '%s: %f' % ('speed=', elapsed_time)
            # print(speed_info)
            cv2.putText(img_org, speed_info, (10, 50),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

            # Put label
            cv2.putText(img_org, pred_label, (10, 100),
                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

            cv2.imshow('han_cho_bot', img_org)
            count = 0

    cam.release()
    cv2.destroyAllWindows()
