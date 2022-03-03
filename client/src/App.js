import React, { useState, useEffect } from "react";
import './App.css';
import Header from './Components/Header';
import Box from '@material-ui/core/Box';



const App = () => {

  return (
    <div className="homepage">
      <div> <Header/></div>
      <div className="video">
        <img
          src="http://127.0.0.1:3001/video_feed"
          alt="Video"
        />
      </div>
      <Box className="glassBox" borderRadius="borderRadius">
      </Box>
    </div>
   );
  };

export default App;
