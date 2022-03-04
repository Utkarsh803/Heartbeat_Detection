
import json, os, requests
import cv2 as cv

subscription_key = "secret_key"

face_api_url = "Endpoint" + '/face/v1.0/detect'

headers = {'Content-Type': 'application/octet-stream','Ocp-Apim-Subscription-Key': subscription_key}

params = {
    'detectionModel': 'detection_03',
    'returnFaceId': 'true'
}



def getRectangle(faceDictionary):
    rect = faceDictionary["faceRectangle"]
    left = int(rect["left"])
    top = int(rect["top"])
    right = left + int(rect["width"])
    bottom = top + int(rect["height"])
    return ((left, top), (right, bottom))


cap = cv.VideoCapture(0)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    is_success, im_buf_arr = cv.imencode(".jpg", frame)
    byte_im = im_buf_arr.tobytes()
    response = requests.post(face_api_url,byte_im,params=params,headers=headers)
    print(response.json())
    faces=json.loads(response.text)
    print("faces", faces)
    for face in faces:
        width,height = getRectangle(face)
        cv.rectangle(frame,width,height,(0,0,170),2)
            #cv2.waitKey(100);
        cv.imshow("campic", frame)
    if cv.waitKey(10) == 27:
        break