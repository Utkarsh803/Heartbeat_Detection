import React, { useEffect, useRef, useState } from "react";
import '../css/Camera.css'
import CameraToggle from './CameraToggle';


const Camera = () => {
    const videoRef = useRef(null);
    const [isShowVideo, setIsShowVideo] = useState(false);
    const videoElement = useRef(null);

  const stopCam = () => {
    let stream = videoElement.current.stream;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    setIsShowVideo(false);
}

    useEffect(() => {
      getVideo();
    }, [videoRef]);

    const getVideo = () => {
      setIsShowVideo(true);
      navigator.mediaDevices
        .getUserMedia({ audio: false, video: {width:(window.innerwidth/2), height: (window.innerwidth/2)} })
        .then(stream => {
          let video = videoRef.current;
          video.srcObject = stream;
          video.play();
        })
        .catch(err => {
          console.error("error:", err);
        });
    }
    return(
      <div>
        <div classname="camera">
          {isShowVideo &&
            <video 
              ref={videoRef}
            />
          }
        </div>
        <div className='toggle'>
          <CameraToggle
          render={({ on, toggle }) => (
            <div>
              { on ?
              <button onClick={getVideo}>Start Video</button>
              :
              <button onClick={stopCam}>Stop Video</button>
            }
            </div>
          )}
          />
        </div>
        <button onClick={getVideo}>Start Video</button>
        <button onClick={stopCam}>Stop Video</button>
        </div>
    );
};
  export default Camera;
