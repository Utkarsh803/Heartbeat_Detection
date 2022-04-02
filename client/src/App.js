import React, { useState, useEffect } from "react";
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
import { SaveDataButton } from "./Components/SaveDataButton";
import Popup from "./Components/Popup";


const App = () => {
  
  
  const [value, setValue] = useState(1)
  const [heartRate, setheartRate] = React.useState(0);
  const [color, setColor] = React.useState(10);


  /*

  useEffect(() => {
    const interval = setInterval(() => fetchData(), 5);
    return () => {
      clearInterval(interval);
    };
  }, []);
  */

  function getColor(heartRate){
    console.log(heartRate);
    if(heartRate<=59 ||heartRate>=101){
      setColor(10);
    console.log("set to 10");
    }
    else if(heartRate>=60 ||heartRate<=100){
      setColor(100);
      console.log("set to 100");
    }
  }
  
  const fetchData =  async () => {
      try {
          const response = await  fetch('http://127.0.0.1:3001/variables');
          if (!response.ok) {throw Error(response.statusText);}
          const json = await response.json();
          setheartRate(json.text);
          console.log(json.text);
          getColor(json.text);

      }
      catch (error) {console.log("Error"+error);}
  }

  useEffect(() => {
    const interval = setInterval(() => {
      fetchData();
    }, 2000)
    return () => clearInterval(interval)
  }, []);
  


  
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
          <div className="glassBox"><Box>
            
          <div className="HRbar">
                 <CircularInput value={value} onChange={setValue}>
                <CircularTrack strokeWidth={5} stroke="#eee" />
                <CircularProgress stroke={`hsl(${value * color}, 100%, 50%)`} />
              </CircularInput>
              </div> 
              <div className="rateinfo">
              <label className="heartrate">{heartRate}</label>
              <label className="shiftLeft">Heart Rate</label>
              </div>
            </Box></div>
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
                <CircularProgress stroke={`hsl(${value * color}, 100%, 50%)`} />
              </CircularInput>
              </div> 
              <div className="rateinfo">
              <label className="heartrate">{heartRate}</label>
              <label className="shiftLeft">Heart Rate</label>
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

