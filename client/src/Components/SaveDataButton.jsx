import React from "react";
import { useState } from "react";
import togglePopup from "./Popup";
import {NotificationManager} from 'react-notifications';

export  const SaveDataButton = () => {
 
    return (
        <button className="saveData" onClick={() => togglePopup()}>Save My Data</button>
    );
}

