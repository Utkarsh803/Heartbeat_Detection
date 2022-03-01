import React, { useState, useEffect } from "react";
import './App.css';
import Header from './Components/Header';
import Box from '@material-ui/core/Box';



const App = () => {

  return (
    <div className="homepage">
      <div> <Header/></div>
      <Box className="glassBox" borderRadius="borderRadius">
      </Box>
    </div>
   );
  };

export default App;
