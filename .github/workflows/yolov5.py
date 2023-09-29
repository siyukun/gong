#!/usr/bin/env python3.6
# encoding: utf-8
import cv2 as cv
from yolov5_trt import YoLov5TRT
import serial
file_yaml = 'coco.yaml'
serial_port = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
if __name__ == "__main__":
    capture = cv.VideoCapture(0)
    capture.set(6, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, 640)
    # a YoLov5TRT instance
    yolov5_wrapper = YoLov5TRT(file_yaml)
    object_0=0
    object_1=0
    object_2=0
    object_3=0
    while capture.isOpened():
        ret, frame = capture.read()
        frame=frame[0:450,170:630]#[0:500,60:520]
        #print(frame.srize())
        if cv.waitKey(1) & 0xFF == ord('q'): break
        frame, use_time,classid,boxs = yolov5_wrapper.infer(frame)
        print(boxs)
        #serial_port.write("\r\n".encode())
        classid_list=classid.tolist()
        for i in classid_list:
            if i ==0:
                #serial_port.write("1\r\n".encode())
                object_0+=1
                print(1)
            elif i==1 or i==2:
                #serial_port.write('2\r\n'.encode())
                object_1+=1
                print(2)
            elif i==3 or i==4 or i==5:
                #serial_port.write('3\r\n'.encode())
                object_2+=1
                print(3)
            elif i==6 or i==7 or i==8:
                #serial_port.write('4\r\n'.encode())
                object_3+=1
                print(4)
        #num=[object_0,object_1,object_2,object_3]
        if object_0>=10:
            serial_port.write("1\r\n".encode())
            object_0=0
            object_1=0
            object_2=0
            object_3=0
            print(111)
        elif object_1>=10:
            serial_port.write("2\r\n".encode())
            object_0=0
            object_1=0
            object_2=0
            object_3=0
            print(222)
        elif object_2>=10:
            serial_port.write("3\r\n".encode())  
            object_0=0
            object_1=0
            object_2=0
            object_3=0 
            print(333) 
        elif object_3>=10:
            serial_port.write("4\r\n".encode())
            object_0=0
            object_1=0
            object_2=0
            object_3=0
            print(444)
        #print(type(object_1))
        #print("object_0:"+chr(object_0)+" object_1:"+chr(object_1)+" object_2:"+chr(object_2)+" object_3:"+chr(object_3))
        #serial_port.write("UART Demonstration Program\r\n".encode())
        #serial_port.write("111\r\n".encode())
        fps = 1.0 / use_time

        text = "FPS : " + str(int(fps))
        cv.putText(frame, text, (20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 1)
        cv.imshow('frame', frame)
    capture.release()
    cv.destroyAllWindows()
    # destroy the instance
    yolov5_wrapper.destroy()
