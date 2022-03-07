
import json, os, requests
import cv2 as cv

class VideoCamera(object):
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        subscription_key = "SECRET_KEY"
        self.face_api_url = "ENDPOINT" + '/face/v1.0/detect'
        self.headers = {'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': subscription_key}
        self.params = {
            'detectionModel': 'detection_03',
            'returnFaceId': 'true'
        }



    def getRectangle(self,faceDictionary):
        rect = faceDictionary["faceRectangle"]
        left = int(rect["left"])
        top = int(rect["top"])
        right = left + int(rect["width"])
        bottom = top + int(rect["height"])
        return ((left, top), (right, bottom))


    def get_frame(self):
        if not self.cap.isOpened:
            print('--(!)Error opening video capture')
            exit(0)
        while True:
            ret, frame = self.cap.read()
            if frame is None:
                print('--(!) No captured frame -- Break!')
                break
            is_success, im_buf_arr = cv.imencode(".jpg", frame)
            byte_im = im_buf_arr.tobytes()
            response = requests.post(self.face_api_url,byte_im,params=self.params,headers=self.headers)
            #print(response.json())
            faces=json.loads(response.text)
            for face in faces:
                width,height = self.getRectangle(face)
                cv.rectangle(frame,width,height,(0,0,170),2)
                    #cv2.waitKey(100);
                ret, jpeg = cv.imencode('.jpg', frame)
                return jpeg.tobytes()
            if cv.waitKey(10) == 27:
                break

