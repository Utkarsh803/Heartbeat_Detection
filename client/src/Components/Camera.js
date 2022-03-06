import React, { useEffect, useRef } from "react";
import '../css/Camera.css'


const Camera = () => {
    const videoRef = useRef(null);

    useEffect(() => {
      getVideo();
    }, [videoRef]);

    const getVideo = () => {
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
        <div classname="camera">
            <video 
              ref={videoRef}
            />
        </div>
    );
};
  export default Camera;
