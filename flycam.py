from pyexpat import model
import sys
import os
import time
import numpy
from time import sleep
import torch
import traceback
import tellopy
import av 
import cv2


model = torch.hub.load('ultralytics/yolov5','iphone_6s_plus_1','./iphone6s/iphone6_best.pt') 
model = torch.hub.load('ultralytics/yolov5','iphone_6s_plus_2','./iphone6s/iphone6_last.pt')
model = torch.hub.load('ultralytics/yolov5','iphone_7_1','./iphone7/iphone7_best.pt')
model = torch.hub.load('ultralytics/yolov5','iphone_7_2','./iphone7/iphone7_last.pt')
model = torch.hub.load('ultralytics/yolov5','iphone_11_1','./iphone11/iphone11_best.pt')
model = torch.hub.load('ultralytics/yolov5','iphone_11_2','./iphone11/iphone11_last.pt')
dir0= './pic'
dir1= './txt1'
dir2= './txt2'

def find_new_file(dir1):
    file_lists = os.listdir(dir1)
    file_lists.sort(key=lambda fn: os.path.getmtime(dir1 + "/" +fn)
                    if not os.path.isdir(dir1 + "/" + fn) else 0)
    file = os.path.join(dir1, file_lists[-1])
    return file

def reset_folder():
    try:
        myfile=dir0+"/1.jpg"
        if os.path.isfile(myfile):
            os.remove(myfile)
    except:
        print("檔案正在給另一個程序使用")
    try:
        myfile=dir0+"/2.jpg"
        if os.path.isfile(myfile):
            os.remove(myfile)
    except:
        print("檔案正在給另一個程序使用")
    try:
        myfile=dir0+"/3.jpg"
        if os.path.isfile(myfile):
            os.remove(myfile)
    except:
        print("檔案正在給另一個程序使用")
    try:
        myfile=dir0+"/4.jpg"
        if os.path.isfile(myfile):
            os.remove(myfile)
    except:
        print("檔案正在給另一個程序使用")
    try:
        myfile=dir0+"/5.jpg"
        if os.path.isfile(myfile):
            os.remove(myfile)
    except:
        print("檔案正在給另一個程序使用")
    try:
        myfile=dir1+"/1.txt"
        if os.path.isfile(myfile):
            os.remove(myfile)
    except:
        print("檔案正在給另一個程序使用")
    try:
        myfile=dir1+"/2.txt"
        if os.path.isfile(myfile):
            os.remove(myfile)
    except:
        print("檔案正在給另一個程序使用")
    try:
        myfile=dir1+"/3.txt"
        if os.path.isfile(myfile):
            os.remove(myfile)
    except:
        print("檔案正在給另一個程序使用")

def env_ctr_drone(drone,run):
    retry = 3
    container = None
    while container is None and 0 < retry:
        retry -= 1
        try:
            container = av.open(drone.get_video_stream())
        except av.AVError as ave:
            print(ave)
    frame_skip = 300
    img_use=0
    cnt=0

    if run == 0:
        with open(dir2+"//3.txt",'w') as f:
            f.write(str(0)+"\n")
        
        drone.takeoff()
        print("takeoff")
        sleep(5)

        drone.clockwise(25)
        print("clockwise")
        sleep(5)
        drone.counter_clockwise(0)
        sleep(2)

    
    for frame in container.iphone(video=0):
        if 0 < frame_skip:
            frame_skip = frame_skip - 1
            continue
        img_use=img_use+1
        image =cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
        if img_use>2:
            img_use=1
        cv2.imwrite("./pic"+str(img_use)+".jpg",image)

        s=0
        if run==0:
            try:
                file=find_new_file(dir1)
                with open(file, encoding='utf8') as f:
                    line = f.readline()
                    wh=float(line.strip())
                    if wh<96:
                        s=5.5
                    elif(wh>=96)and(wh<(96+10)):
                        s=4.5
                    else:
                        s=3.5
                    print("s=",s)
                
                reset_folder()

            except:
                cnt-cnt
                    
        if(s>0)and(run==0):
            drone.forward(25)
            print("forward")
            sleep(5)
            drone.backward(0)
            print("backward")
            sleep(2)

            file=find_new_file(dir2)
            with open(file, encoding='utf8') as f:
                line = f.readline()
                p=int(line.strip())
                print("p=",p)
            with open(dir2+"//3.txt",'w') as f:
                f.write(str(p+1)+"\n")

            break   
        s=0

        if (run==0):
            try:
                with open(file, encoding='utf8') as f:
                    line = f.readline()
                    wh=float(line.strip())
                    if wh<96:
                        s=5.5
                    elif(wh>=96)and(wh<(96+10)):
                        s=4.5
                    else:
                        s=3.5
                    print("s=",s)
                reset_folder()
            except:
                cnt=cnt

        if(s>0)and(run==1):
            drone.forward(25)
            print("forward")
            sleep(s)
            drone.backward(0)
            print("backward")
            sleep(2)

            file=find_new_file(dir2)
            with open(file, encoding='utf8') as f:
                line = f.readline()
                p=int(line.strip())
                print("p=",p)
            with open(dir2+"//3.txt",'w') as f:
                f.write(str(p+1)+"\n")
                
            break   
    
        s=0

        if(s>0)and (run==2):
            drone.forward(25)
            print("forward")
            sleep(s)
            drone.backward(0)
            print("backward")
            sleep(2)
            drone.counter_clockwise(25)
            print("counter_clockwise")
            sleep(9)
            drone.clockwise(0)
            print("clockwise")
            sleep(2) # degree

            drone.forward(25)
            print("forward")
            sleep(s)
            drone.backward(0)
            print("backward")
            sleep(2)
            drone.land(0)
            print("land")
            sleep(2)

            break

        cnt=cnt+1
        print("cnt=",cnt)

    reset_folder()

reset_folder()

drone = tellopy.Tello()
try:
    drone.connect()
    drone.wait_for_connection(10.0)
    for run in range(0,2,1):
        env_ctr_drone(drone,run)
except Exception as ex :
    exc_type,exc_value,exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type,exc_value,exc_traceback)
    print(ex)
finally:
    drone.quit()