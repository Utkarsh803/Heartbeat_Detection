#from _future_ import print_function
import cv2 as cv
import argparse



class camera(object):
    face_cascade = ''
    eyes_cascade = ''
    parser = ''
    frame = ''
    args = ''
    camera_device=''
    cap=''
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
        #parser.add_argument('--face_cascade', help='Path to face cascade.', default='data/haarcascades/haarcascade_frontalface_alt.xml')
        #parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
        self.parser.add_argument('--face_cascade', help='Path to face cascade.', default='haarcascade_frontalface_alt.xml')
        self.parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='haarcascade_eye_tree_eyeglasses.xml')
        self.parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
        self.args = self.parser.parse_args()
        self.face_cascade_name = self.args.face_cascade
        self.eyes_cascade_name = self.args.eyes_cascade
        #global self.face_cascade
        self.face_cascade = cv.CascadeClassifier()
        #global self.eyes_cascade
        self.eyes_cascade = cv.CascadeClassifier()    
        #-- 1. Load the cascades
        if not self.face_cascade.load(cv.samples.findFile(self.face_cascade_name)):
            print('--(!)Error loading face cascade')
            exit(0)
        if not self.eyes_cascade.load(cv.samples.findFile(self.eyes_cascade_name)):
            print('--(!)Error loading eyes cascade')
            exit(0)
        self.camera_device = self.args.camera
        #-- 2. Read the video stream
        self.cap = cv.VideoCapture(self.camera_device)

    def face_detection(self): 
        if not self.cap.isOpened:
            print('--(!)Error opening video capture')
            return -2
        #while True:
        ret, self.frame = self.cap.read()
        if self.frame is None:
            print('--(!) No captured self.frame -- Break!')
            return -1
        self.frame = self.detectAndDisplay()
        ret, jpeg = cv.imencode('.jpg', self.frame)
        return jpeg.tobytes()
            #break


    def detectAndDisplay(self):
        self.frame_gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)
        self.frame_gray = cv.equalizeHist(self.frame_gray)
        #-- Detect faces
        faces = self.face_cascade.detectMultiScale(self.frame_gray)
        for (x,y,w,h) in faces:
            center = (x + w//2, y + h//2)
            self.frame = cv.ellipse(self.frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
            faceROI = self.frame_gray[y:y+h,x:x+w]
            #-- In each face, detect eyes
            eyes = self.eyes_cascade.detectMultiScale(faceROI)
            for (x2,y2,w2,h2) in eyes:
                eye_center = (x + x2 + w2//2, y + y2 + h2//2)
                radius = int(round((w2 + h2)*0.25))
                self.frame = cv.circle(self.frame, eye_center, radius, (255, 0, 0 ), 4)
        cv.imshow('Capture - Face detection', self.frame)
        return self.frame # in the form numpy.ndarray

# END OF CODE



