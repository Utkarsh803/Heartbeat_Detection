from flask import Flask,render_template,Response
import cv2
from flask import jsonify
from main import camera
from flask_cors import CORS, cross_origin

app=Flask(__name__)
VC=camera()
CORS(app)

global open
open=1


camera2=cv2.VideoCapture(0)
def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera2.read()
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('App.js')

@app.route('/video_feed')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.face_detection()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
               
@app.route('/video')
def video_feed():
    return Response(gen(VC),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def getvar(camera):
    global open
    if open==1:
        while True:
            frame = camera.get_variables()
            return frame

@app.route('/variables')
def variables():
    return jsonify({'text': getvar (VC)})  

def stopCam(camera):
        stop = camera.__del__()
       

@app.route('/stop')
def stop():
    global open
    VC.__del__()
    open=0
    print("Deleting...")
    return "Nothing"

@app.route('/start')
def start():
    global open
    open=1
    return "Nothing"

if __name__ == '__main__':
    app.run(port=3001, threaded=True, use_reloader=False)