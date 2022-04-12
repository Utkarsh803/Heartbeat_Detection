# from _future_ import print_function

from scipy import signal
import neurokit2 as nk
import cv2 as cv
import argparse
import imageManipulation
import numpy as np
import matplotlib.pyplot as plt
import time

class camera(object):
    face_cascade = ''
    eyes_cascade = ''
    parser = ''
    frame = ''
    args = ''
    camera_device = ''
    cap = ''
    ROI = None
    ROI1 = None
    arr = []
    startX = 0
    startY = 0
    y = 0
    firstLine = 0
    endX = 0
    rgb_arr = []
    red_arr=[]
    blue_arr=[]
    green_arr=[]
    red=0
    green=0
    window=False
    blue = 0
    heartrate=0
    frames=0
    finalHr=0
    heartbeatArray=[]
    hrNum=0
    curve=[]
    interval=0
    prev_frame_time = 0
    new_frame_time = 0
    framesPerSecond=0

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
        # parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/haarcascades/haarcascade_frontalface_alt.xml')
        # parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
        self.parser.add_argument('--face_cascade', help='Path to face cascade.',
                                 default='haarcascade_frontalface_alt.xml')
        self.parser.add_argument('--eyes_cascade', help='Path to eyes cascade.',
                                 default='haarcascade_eye_tree_eyeglasses.xml')
        self.parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
        self.args = self.parser.parse_args()
        self.face_cascade_name = self.args.face_cascade
        self.eyes_cascade_name = self.args.eyes_cascade
        # global self.face_cascade
        self.face_cascade = cv.CascadeClassifier()
        # global self.eyes_cascade
        self.eyes_cascade = cv.CascadeClassifier()
        # -- 1. Load the cascades
        if not self.face_cascade.load(cv.samples.findFile(self.face_cascade_name)):
            print('--(!)Error loading face cascade')
            exit(0)
        if not self.eyes_cascade.load(cv.samples.findFile(self.eyes_cascade_name)):
            print('--(!)Error loading eyes cascade')
            exit(0)
        self.ROI = None
        self.framesPerSecond=0
        self.heartrate=0
        self.finalHr=0
        self.ROI2=None
        self.ROI1=None
        self.frames=360
        self.startX = 0
        self.startY = 0
        self.y = 0
        self.endX = 0
        self.firstLine = 0
        self.arr =[]
        self.rgb_arr = []
        self.red_arr= [0] * (self.frames)
        self.green_arr=[0] * (self.frames)
        self.blue_arr = [0] * (self.frames)
        self.red=0
        self.green=0
        self.window=False
        self.blue = 0
        self.framecount = 0
        self.camera_device = self.args.camera
        self.heartbeatArray=[0] * 10
        self.hrNum=0
        self.curve=[]
        self.interval=0
        self.prev_frame_time = 0
        self.new_frame_time = 0
        # -- 2. Read the video stream
        self.cap = cv.VideoCapture(0)

    def get_variables(self):
        result=self.finalHr
        return str(result)

    def get_curve(self):
        if len(self.curve):
            return self.curve
        else:
            return [0]

    def __del__(self):
        try: 
            self.cap.stop()
            self.cap.release()
        except:
            print('probably there\'s no cap yet :(')
        cv.destroyAllWindows()

    def get_heartrate(self, sig):
       # smooth_sig=imageManipulation.signal_smooth(sig)
        
        #detrend signal
        dtr_sig = signal.detrend(sig)

        #normalize
        norm_sig = imageManipulation.z_normalize(dtr_sig)
        self.curve=norm_sig 
       
        #get source signals 
        norm_sig=np.transpose(norm_sig)
        real_sig=imageManipulation.ica(norm_sig)
        
        #calculate fft
        fft = np.abs(np.fft.fft(real_sig, axis=0))**2
        freq = np.fft.fftfreq(self.frames, 1.0 / self.framesPerSecond)
        maxPower = np.max(fft, axis=1)
        idx = np.where((freq >= 1) & (freq <= 2))
        Pwr = maxPower[idx]
        Freqs = freq[idx]
        Iddx = np.argmax(Pwr)
        hr = Freqs[Iddx]
        return hr*60

    def face_detection(self):
        if not self.cap.isOpened:
            print('--(!)Error opening video capture')
            return -2
        # while True:
        ret, self.frame = self.cap.read()
        self.new_frame_time = time.time()
        fps = 1/(self.new_frame_time-self.prev_frame_time)
        fps = int(fps)
        self.framesPerSecond=fps
        fps = "FPS: "+str(fps)
        font = cv.FONT_HERSHEY_SIMPLEX
        cv.putText(self.frame, fps, (7, 70), font, 1, (100, 255, 0), 3, cv.LINE_AA)
        text= "Please stay still"
        cv.putText(self.frame, text, (7, 470), font, 1, (100, 255, 0), 3, cv.LINE_AA)
        self.prev_frame_time = self.new_frame_time
        if self.frame is None:
            print('--(!) No captured self.frame -- Break!')
            return -1
        self.frame = self.detectAndDisplay()
        ret, jpeg = cv.imencode('.jpg', self.frame)
        return jpeg.tobytes()
        # break


    def most_frequent(self,List):
        Fcounter = 0
        num = List[0]
        for i in List:
            curr_frequency = List.count(i)
            if(curr_frequency> Fcounter):
                Fcounter = curr_frequency
                num = i
        return num


    def detectAndDisplay(self):
        self.frame_gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        self.frame_gray = cv.equalizeHist(self.frame_gray)

        # -- Detect faces
        faces = self.face_cascade.detectMultiScale(self.frame_gray)

        for (x, y, w, h) in faces:
            self.y = y
            center = (x + w // 2, y + h // 2)
            faceROI = self.frame_gray[y:y + h, x:x + w]
            startpointX = (x + w) - x
            areaNeedX = 0.50 * startpointX
            cutareaX = startpointX - areaNeedX
            partitionX = cutareaX / 2
            self.startX = x + int(partitionX)
            self.endX = (x + w) - int(partitionX)

            startpointY = (y + h) - y
            areaNeedY = 0.90 * startpointY
            cutareaY = startpointX - areaNeedY
            partitionY = cutareaY / 2
            self.startY = y + int(partitionY)
            endY = (y + h) - int(partitionY)

            totalHeight = (y + h) - y
            self.firstLine = 0.20 * totalHeight
            secondLine = 0.55 * totalHeight
            cv.rectangle(self.frame, (self.startX - 10, self.startY - 10),
                         (self.endX + 10, y + int(self.firstLine) + 10), (255, 0, 0), 2)

        if self.framecount < self.frames:
            self.framecount = self.framecount + 1

        
        self.ROI = self.frame[self.startY:self.y + int(self.firstLine), self.startX:self.endX]


        
        red, green, blue=imageManipulation.calc_avg_rgb(self.ROI)


        if self.window==False and self.framecount<len(self.red_arr):
            self.red_arr[self.framecount]=red
            self.green_arr[self.framecount]=green
            self.blue_arr[self.framecount]=blue

        if self.window==True:
            self.interval=self.interval+1
            count=1
            for i in self.red_arr:
                if count < len(self.red_arr):
                    self.red_arr[count-1]=self.red_arr[count]
                    self.green_arr[count-1]=self.green_arr[count]
                    self.blue_arr[count-1]=self.blue_arr[count]
                    count=count+1
                else: 
                    self.red_arr[count-1]=red
                    self.green_arr[count-1]=green
                    self.blue_arr[count-1]=blue
            


        if self.framecount >=self.frames :
            self.rgb_arr=np.matrix([self.red_arr,self.blue_arr,self.green_arr])
            if self.interval>=12 or self.window==False:
                self.heartrate = (int)(self.get_heartrate(self.rgb_arr))
                self.interval=0

                if self.hrNum < 10:
                    self.heartbeatArray[self.hrNum]=self.heartrate
                    self.hrNum=self.hrNum+1
            
                if self.hrNum >= 10:
                    hrcount=1
                    for i in self.heartbeatArray:
                        if hrcount < len(self.heartbeatArray):
                            self.heartbeatArray[hrcount-1]=self.heartbeatArray[hrcount]
                            hrcount=hrcount+1
                        else:
                            self.heartbeatArray[hrcount-1]=self.heartrate
                
                self.finalHr=self.most_frequent(self.heartbeatArray)
               # self.finalHr=max(self.heartbeatArray)

            self.window=True



        cv.imshow('Capture - Face detection', self.frame)
        return self.frame  # in the form numpy.ndarray

    # END OF CODE



#cam = camera()
#while True:
#   cam.face_detection()


