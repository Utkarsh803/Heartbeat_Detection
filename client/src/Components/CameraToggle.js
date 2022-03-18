import React, { Component } from "react";
import '../css/CameraToggle.scss';

class CameraToggle extends Component {
    render() {
     return (
         <>
         <div className="camera-toggle">
         <input 
         type="checkbox" 
         className="camera-toggle-checkbox" 
         name="cameraToggle"
         id="cameraToggle"
         />
         <label className="camera-toggle-label" htmlFor="cameraToggle">
             <span className="camera-toggle-inner"/>
             <span className="camera-toggle-switch"/>
         </label>
         </div>
         </>
     );
    }
}

export default CameraToggle;