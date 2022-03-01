from flask import Flask, render_template, Response, make_response
from numpy import VisibleDeprecationWarning
#from camera import VideoCamera
from flask import jsonify
import cv2;
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

#VC=VideoCamera()

@app.route('/')
def index():
    return render_template('App.js')


if __name__ == '__main__':
    app.run(port=3001, threaded=True, use_reloader=False)