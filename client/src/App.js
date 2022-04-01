import React, { useState } from "react";
import { PageLayout } from "./Components/PageLayout";
import './App.css';
import Header from './Components/Header';
import Box from '@material-ui/core/Box';
import Camera from './Components/Camera';
import { AuthenticatedTemplate, UnauthenticatedTemplate, useMsal } from "@azure/msal-react";
import { loginRequest } from "./authConfig";
import Button from "react-bootstrap/Button";
import { ProfileData } from "./Components/ProfileData";
import { callMsGraph } from "./graph";
import CameraToggle from './Components/CameraToggle';
import {
	CircularInput,
	CircularTrack,
	CircularProgress,
	CircularThumb
} from 'react-circular-input'



const App = () => {
  
  
  const [value, setValue] = useState(0.50)
  const [heartRate, setheartRate] = React.useState(0);
  
  
  
  
  return (
<div>
    <AuthenticatedTemplate>
  <div>
        <div className="homepage">
          <div><Header/></div>
            <div className="toggle">
            <CameraToggle/>
            </div>
          <div className="video">
          <img
            src="http://127.0.0.1:3001/video"
            alt="Video"
          />
          <div className="glassBox"><Box></Box></div>
        </div>
            </div>
            </div>
            </AuthenticatedTemplate>
            <UnauthenticatedTemplate>
            <div>
             <div className="homepage">
              <div><Header/></div>
            <div className="toggle">
            <CameraToggle/>
            </div>
               <div className="video">
               <img
                 src="http://127.0.0.1:3001/video"
                 alt="Video"
               />
               <div className="glassBox"><Box>
               
               <div className="HRbar">
                 <CircularInput value={value} onChange={setValue}>
                <CircularTrack strokeWidth={5} stroke="#eee" />
                <CircularProgress stroke={`hsl(${value * 100}, 100%, 50%)`} />
              </CircularInput>
              </div> 
              <div className="rateinfo">
              <label className="heartrate">{heartRate}</label>
              <label >Heart Rate</label>
              </div>
                 </Box></div>
             </div>
                 </div> 
                 </div>  
            </UnauthenticatedTemplate>
            </div>       
   );
  };


/*
pageLayout
<AuthenticatedTemplate>
  **code**    
</AuthenticatedTemplate>
      <UnauthenticatedTemplate>
                <h5 className="card-title">Please sign-in to see your profile information.</h5>
            </UnauthenticatedTemplate>
*/
export default App;

