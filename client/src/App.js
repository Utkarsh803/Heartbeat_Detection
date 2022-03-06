import React from "react";
import './App.css';
import Header from './Components/Header';
import Box from '@material-ui/core/Box';
import Camera from './Components/Camera';


const App = () => {
  return (
    <div className="homepage">
      <div><Header/></div>
      <div><Camera/></div>
      <div><Box className="glassBox" borderRadius="borderRadius"/></div>
    </div>
   );
  };

export default App;

