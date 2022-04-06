# from _future_ import print_function
from scipy import signal
import neurokit2 as nk
import cv2 as cv
import argparse
import imageManipulation
import numpy as np
import matplotlib.pyplot as plt

class camera(object):
    face_cascade = ''
    eyes_cascade = ''
    parser = ''
    frame = ''
    args = ''
    camera_device = ''
    cap = ''
    ROI = None
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
        self.heartrate=72
        self.finalHr=0
        self.frames=150
        self.startX = 0
        self.startY = 0
        self.y = 0
        self.endX = 0
        self.firstLine = 0
        self.arr =[]
        self.rgb_arr = []
        self.red_arr= [0] * (self.frames+1)
        self.green_arr=[0] * (self.frames+1)
        self.blue_arr = [0] * (self.frames+1)
        self.red=0
        self.green=0
        self.window=False
        self.blue = 0
        self.framecount = 0
        self.camera_device = self.args.camera
        self.heartbeatArray=[0] * 20
        self.hrNum=0
        # -- 2. Read the video stream
        self.cap = cv.VideoCapture(self.camera_device)

    def get_variables(self):
        result=self.heartrate
        return str(result)

    def __del__(self):
        try: 
            self.cap.stop()
            self.cap.release()
        except:
            print('probably there\'s no cap yet :(')
        cv.destroyAllWindows()

    def get_heartrate(self, sig):

        dtr_sig = signal.detrend(sig)
       # print("Detrended",dtr_sig)

        norm_sig = imageManipulation.z_normalize(dtr_sig)
        #print("normalised", norm_sig)
       
        #apply ica       
        ica_sig=imageManipulation.ica(norm_sig)
        real_sig=np.dot(ica_sig,norm_sig)
        
        #apply fft
        L=len(real_sig[2])
        raw = np.fft.rfft(real_sig[2])
        freqs = float(30) / L * np.arange(L / 2 + 1)
        freqs2 = 60. * freqs
        fft = np.abs(raw)**2
        idx = np.where((freqs2 > 60) & (freqs2 < 120))
        pruned = fft[idx]
        pfreq = freqs[idx]
        freqs = pfreq
        fft = pruned
        idx2 = np.argmax(pruned)
        bpm = freqs[idx2]
        return bpm * 60

    def face_detection(self):
        if not self.cap.isOpened:
            print('--(!)Error opening video capture')
            return -2
        # while True:
        ret, self.frame = self.cap.read()
        if self.frame is None:
            print('--(!) No captured self.frame -- Break!')
            return -1
        self.frame = self.detectAndDisplay()
        ret, jpeg = cv.imencode('.jpg', self.frame)
        return jpeg.tobytes()
        # break

    def get_fps2(self):
        fps = self.cap.get(cv.CAP_PROP_FPS)
        return fps

    def mostFrequent(self,arr, n):
        # Sort the array
        arr.sort()
    
        # find the max frequency using
        # linear traversal
        max_count = 1; res = arr[0]; curr_count = 1
        
        for i in range(1, n):
            if (arr[i] == arr[i - 1]):
                curr_count += 1
                
            else :
                if (curr_count > max_count):
                    max_count = curr_count
                    res = arr[i - 1]
                
                curr_count = 1
        
        # If last element is most frequent
        if (curr_count > max_count):
            max_count = curr_count
            res = arr[n - 1]
        
        return res

    def detectAndDisplay(self):
        self.frame_gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        self.frame_gray = cv.equalizeHist(self.frame_gray)

        # -- Detect faces
        faces = self.face_cascade.detectMultiScale(self.frame_gray)

        for (x, y, w, h) in faces:
            self.y = y
            center = (x + w // 2, y + h // 2)
            # self.frame = cv.ellipse(self.frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
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
            cv.rectangle(self.frame, (self.startX + 10, self.startY + 10),
                         (self.endX + 10, y + int(self.firstLine) + 10), (255, 0, 0), 2)
        if self.framecount < self.frames:
            self.framecount = self.framecount + 1
        #print("frame", self.framecount)
        
        self.ROI = self.frame[self.startY:self.y + int(self.firstLine), self.startX:self.endX]

        red, green, blue=imageManipulation.calc_avg_rgb(self.ROI)

       # self.rgb_arr.append(imageManipulation.calc_avg_col(self.ROI))

        if self.window==False:
            self.red_arr[self.framecount]=red
            #print(self.framecount)
            self.green_arr[self.framecount]=green
            self.blue_arr[self.framecount]=blue

        if self.window==True:
            count=1
            for i in self.red_arr:
                if count < len(self.red_arr):
                    self.red_arr[count-1]=self.red_arr[count]
                # print(self.framecount)
                    self.green_arr[count-1]=self.green_arr[count]
                    self.blue_arr[count-1]=self.blue_arr[count]
                    count=count+1
                else:
                    
                    self.red_arr[count-1]=red
                    #print(self.framecount)
                    self.green_arr[count-1]=green
                    self.blue_arr[count-1]=blue
            


        if self.framecount >=self.frames :
            self.rgb_arr=np.matrix([self.red_arr,self.blue_arr,self.green_arr])
           # print(self.rgb_arr)
            self.heartrate = (int)(self.get_heartrate(self.rgb_arr))


            if self.hrNum < 20:
                self.hrNum=self.hrNum+1
                self.heartbeatArray[self.hrNum]=self.heartrate
                self.hrNum=self.hrNum+1
            if self.hrNum >= 20:
                count=1
                for i in self.heartbeatArray:
                    if count < len(self.heartbeatArray):
                        self.heartbeatArray[count-1]=self.heartbeatArray[count]
                        count=count+1
                    else:
                        self.heartbeatArray[count-1]=self.heartrate
            #self.finalHr=self.mostFrequent(self.heartbeatArray, 20)
            self.finalHr=max(self.heartbeatArray)
            print("----heartrate----", self.finalHr)
            self.window=True
        #if self.framecount == 200:
        #    tmp = self.rgb_arr[100:len(self.rgb_arr)-1]
        #    self.rgb_arr.clear()
        #    self.rgb_arr = tmp
        #    self.framecount = 100
        
        cv.imshow('Capture - Face detection', self.frame)
        return self.frame  # in the form numpy.ndarray

    # END OF CODE



#cam = camera()
#while True:
#   cam.face_detection()


