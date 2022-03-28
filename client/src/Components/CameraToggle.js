import React, {Component} from 'react'
import Switch from 'react-switch'

export default function CameraToggle() {
    const [cameraOn, setState] = React.useState(true);

    const handleSwitch = (event) => {
        setState(event.target.checked);
      };
    
      return (
        <Switch
          cameraOn={cameraOn}
          onChange={handleSwitch}
        />
      );
    }