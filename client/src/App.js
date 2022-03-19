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



const App = () => {
  return (
//    <PageLayout>
      <div>
      <a>
        <div className="homepage">
          <div><Header/></div>
          <div className="video">
          <img
            src="http://127.0.0.1:3001/video_feed"
            alt="Video"
          />
          </div>
          <div className="glassBox"><Box></Box></div>
        </div>
      </a>
            </div>
//    </PageLayout>
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

