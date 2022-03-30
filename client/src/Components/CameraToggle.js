import * as React from 'react'
import Switch from '@mui/material/Switch';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';

export default function CameraToggle() {

  const [camera, setCamera] = React.useState(true);

  const handleChange = (event) => {
    setCamera(event.target.camera);
  };
  
      return (
        <FormControl component="fieldset">
        <FormGroup aria-label="position" row>
        <FormControlLabel
          value="start"
          control={<Switch camera={camera}
          onChange={handleChange} color="primary" />}
          label="Camera"
          labelPlacement="start"
        />
        </FormGroup>
        </FormControl>
      );
    }