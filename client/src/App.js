import React, { useState, useEffect } from "react";
import './App.css';
import Header from './Components/Header';
import Box from '@material-ui/core/Box';



const App = () => {

  return (
    <div className="homepage">
      <div> <Header/></div>
      <div style={{ marginLeft: window.innerWidth / 2, marginTop: '90px', width: (window.innerWidth / 2) - 20, height: window.innerHeight }}>
      <Box color="white" bgcolor="darkgrey" p={50}>
      </Box>
      </div>
    </div>

   );
  };

export default App;
