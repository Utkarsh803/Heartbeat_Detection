import React from "react";
import './App.css';
import Header from './Components/Header';
import Box from '@material-ui/core/Box';
import Camera from './Components/Camera';


const App = () => {
  return (
    <div className="homepage">
      <div><Header/></div>
      <div className="video">
      <img
        src="http://127.0.0.1:3001/video"
        alt="Video"
      />
      </div>
      <div className="glassBox"><Box></Box></div>
      </div>
   );
  };

export default App;

