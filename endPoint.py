
from flask import Flask,render_template,Response
import cv2
from flask import jsonify
from main import camera
from flask_cors import CORS, cross_origin
from flask import request
from database import db
import json
import pandas as pd


app=Flask(__name__)
VC=camera()
dbase=db()
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


@app.route('/post')
def my_route():
  email = request.args.get('email', type = str)
  hr = request.args.get('hr', type = int)
  dat=request.args.get('dat', type = str)
  dbase.data_entry(email, hr, dat)
  data = "success"
  return jsonify({"text": data})

#http://127.0.0.1:3001/fetch/fadasda
@app.route('/fetch/<usremail>', methods=['GET'])
def fetch(usremail):
  #email = request.args.get('email', type = str)
  #email="sdjnsdkjv"
  lis=[['heartbeat', 'date', 'id']]
  hrtbt=[]
  dattlist=[]
  iidList=[]
  rows=dbase.query_table(usremail)
  for row in rows:
      hrt=row[0]
      hrtbt.append(hrt)
      datt=row[1]
      dattlist.append(datt)
      datt=datt.strftime("%Y-%m-%d")
      iid=row[2]
      iidList.append(iid)
      lis.append([hrt,datt,iid])
  out = [dict(zip(lis[0], row)) for row in lis[1:]]  
  return jsonify(out)


if __name__ == '__main__':
    app.run(port=3001, threaded=True, use_reloader=False)