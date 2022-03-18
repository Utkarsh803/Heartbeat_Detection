import React from "react";
import { PageLayout } from "./Components/PageLayout";
import './App.css';
import Header from './Components/Header';
import Box from '@material-ui/core/Box';
import Camera from './Components/Camera';


const App = () => {
  return (
    <PageLayout>
      <a>
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
      </a>
    </PageLayout>
   );
  };

export default App;

