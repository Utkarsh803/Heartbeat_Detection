import React, {Component, useState, useEffect} from "react";
import {useContext} from 'react';
import '../css/Header.css'
import logo from '../assets/mslogo.jpg'
import '../css/CameraToggle.scss'
import CameraToggle from "./CameraToggle";
import { callMsGraph } from "../graph";
import { ProfileData } from "./ProfileData";
import { AuthenticatedTemplate, UnauthenticatedTemplate, useMsal } from "@azure/msal-react";
import { loginRequest } from "../authConfig";

const Header = () => {
    // Sticky Menu Area
    useEffect(() => {
      window.addEventListener("scroll", isSticky);
      return () => {
        window.removeEventListener("scroll", isSticky);
      };
    });
  
    /* Method that will fix header after a specific scrollable */
    const isSticky = (e) => {
      const header = document.querySelector(".header");
      const scrollTop = window.scrollY;
      scrollTop >= 250
        ? header.classList.add("is-sticky")
        : header.classList.remove("is-sticky");
    };


function ProfileContent() {
  const { instance, accounts } = useMsal();
  const [graphData, setGraphData] = useState(null);

  const name = accounts[0] && accounts[0].name;
function RequestProfileData() {
      const request = {
          ...loginRequest,
          account: accounts[0]
      };

      // Silently acquires an access token which is then attached to a request for Microsoft Graph data
      instance.acquireTokenSilent(request).then((response) => {
          callMsGraph(response.accessToken).then(response => setGraphData(response));
      }).catch((e) => {
          instance.acquireTokenPopup(request).then((response) => {
              callMsGraph(response.accessToken).then(response => setGraphData(response));
          });
      });
  }

  return (
      <>
          <span>Welcome {name}</span>
      </>
  );
};


    return (
      <>
        <header className="header">
        <img src={logo}></img>
        <div className="username"><ProfileContent /></div>
        <button  className="button">
          Sign Out
        </button>
        <camera-toggle className="camera-toggle"><CameraToggle></CameraToggle></camera-toggle>
        </header>
      </>
    );
  };
  
  export default Header;