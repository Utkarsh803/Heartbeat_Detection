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
      <div style={{ marginLeft: (window.innerWidth / 2) + 10, marginTop: '90px', width: (window.innerWidth / 2) - 40 }}>
      <Box bgcolor="#f4f4f4" boxShadow="5px 5px 5px #b2b2b3" p={50} borderRadius="borderRadius">
      </Box>
      </div>
    </div>

   );
  };

export default App;
