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
    blue = 0
    heartrate=0

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
        self.startX = 0
        self.startY = 0
        self.y = 0
        self.endX = 0
        self.firstLine = 0
        self.arr = np.full(
            shape=(3,50),
            fill_value=0,
            dtype=np.int
        )
        self.rgb_arr = []
        self.red_arr=[]
        self.green_arr=[]
        self.blue_arr = []
        self.red=0
        self.green=0
        self.blue = 0
        self.framecount = 0
        self.camera_device = self.args.camera
        # -- 2. Read the video stream
        self.cap = cv.VideoCapture(self.camera_device)

    def get_variables(self):
        result=self.heartrate
        return str(result)

    def __del__(self):
        try: 
            self.cap.stop()
            self.cap.stream.release()
        except:
            print('probably there\'s no cap yet :(')
        cv.destroyAllWindows()

    def get_heartrate(self, sig):
        dtr_sig = signal.detrend(sig)
        norm_sig = imageManipulation.z_normalize(dtr_sig)
        interpolated = np.hamming(len(norm_sig)) * norm_sig
        fft = np.fft.rfft(interpolated, n= len(interpolated))
        threshold = 0.3 * max(abs(fft))
        peaks = signal.find_peaks(fft,height= threshold)
        print("Threshold =",threshold,"  Peaks =",len(peaks[0])," framcount =",self.framecount)
        freq = len(peaks[0]) / (self.framecount/30) # time = num frames / fps
        return freq * 60

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
        self.framecount = self.framecount + 1
        self.ROI = self.frame[self.startY:self.y + int(self.firstLine), self.startX:self.endX]
#
#        self.rgb_arr.append(imageManipulation.calc_avg_col(self.ROI))
#
#        if self.framecount >= 50 and self.framecount%10 == 0:
#
 #           heartrate = self.get_heartrate(self.rgb_arr)
  #          print("----heartrate----", heartrate)
   #     if self.framecount == 200:
    #        tmp = self.rgb_arr[100:len(self.rgb_arr)-1]
     #       self.rgb_arr.clear()
      #      self.rgb_arr = tmp
       #     self.framecount = 100

        cv.imshow('Capture - Face detection', self.frame)
        return self.frame  # in the form numpy.ndarray

    # END OF CODE



#cam = camera()
#while True:
#   cam.face_detection()
