import React, { useState, useEffect, useRef } from "react";
import { PageLayout } from "./Components/PageLayout";
import './App.css';
import Header from './Components/Header';
import Box from '@material-ui/core/Box';
import Camera from './Components/Camera';
import { AuthenticatedTemplate, MsalAuthenticationTemplate, UnauthenticatedTemplate, useIsAuthenticated, useMsal} from "@azure/msal-react";
import { loginRequest } from "./authConfig";
import Button from "react-bootstrap/Button";
import { ProfileData } from "./Components/ProfileData";
import { callMsGraph } from "./graph";
import CameraToggle from './Components/CameraToggle';
import {
	CircularInput,
	CircularTrack,
	CircularProgress,
	CircularThumb
} from 'react-circular-input'
import { SaveDataButton } from "./Components/SaveDataButton";
import { msalConfig } from "./authConfig";
import ScrollButton from "./Components/ScrollButton";
import "./css/styles.css"
import Chart, {
  ArgumentAxis,
  Legend,
  Series,
  ValueAxis,
  Label,
  Export,
  Tick,
} from 'devextreme-react/chart';


 function App  ()  {
  const isAuthenticated = useIsAuthenticated();
  const [value, setValue] = useState(1)
  const [heartRate, setheartRate] = React.useState(0);
  const [color, setColor] = React.useState(10);
  const [datt, setDate] = React.useState(0);
  const [table, setTable] = useState([{"date":"DATE","heartbeat":"HEARTBEAT","id":"ID"}]);
  const [track, setTrack] = useState('');
  const [showtable, setshowTable] = useState(false); 
  const { instance, accounts } = useMsal();
  const accId = accounts[0] ? accounts[0].username : null;
  const titleRef = useRef();
  



   function ProfileContent () {
    const [graphData, setGraphData] = useState(null);   
    const name = accounts[0] && accounts[0].username;
    function RequestProfileData() {
      const request = {
        ...loginRequest,
        account: accounts[0]
      };
  
      // Silently acquires an access token which is then attached to a request for Microsoft Graph data
      instance.acquireTokenSilent(request).then((response) => {
        callMsGraph(response.accessToken).then(response => setGraphData(response));
      }).catch((e) => {
        instance.acquireTokenPopup(request).then((response) => {
          callMsGraph(response.accessToken).then(response => setGraphData(response));
        });
      });
    }
    setName(name);
    console.log("newname------", name);
    return name
  };
  

  /*

  useEffect(() => {
    const interval = setInterval(() => fetchData(), 5);
    return () => {
      clearInterval(interval);
    };
  }, []);
  */

  function getColor(heartRate){
    console.log(heartRate);
    if(heartRate<=59 ||heartRate>=101){
      setColor(10);
    console.log("set to 10");
    }
    else if(heartRate>=60 ||heartRate<=100){
      setColor(100);
      console.log("set to 100");
    }
  }

  const postHeartrate =  async () => {
    try {
        const usrname=accId;
        var today = new Date();
        var dd = String(today.getDate()).padStart(2, '0');
        var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
        var yyyy = today.getFullYear();
        today = yyyy + '-' + mm + '-' + dd;
        const url='http://127.0.0.1:3001/post?email='+usrname+'&hr='+heartRate+'&dat='+today;
        const response = await  fetch(url);
        if (!response.ok) {throw Error(response.statusText);}
        const json = await response.json();
        console.log("--------------------------------success", json.text)
        console.log(json.text);
        
      
    }
    catch (error) {console.log("Error"+error);}
}

function setName(name){
  accId=name;
}

function setName(){
  return accId;
}

const fetchHeartrate = async() => {
  try {
      const usrname=accId;
      const url='http://127.0.0.1:3001/fetch/'+usrname;
      const response = await  fetch(url);
      if (!response.ok) {throw Error(response.statusText);}
      const json = await response.json();
      setTable(json);
      console.log("the json ----------------------",json);
  }
  catch (error) {console.log("Error"+error);}
}
 

  const fetchData =  async () => {
      try {
          const response = await  fetch('http://127.0.0.1:3001/variables');
          if (!response.ok) {throw Error(response.statusText);}
          const json = await response.json();
          setheartRate(json.text);
          console.log(json.text);
          getColor(json.text);
      }
      catch (error) {console.log("Error"+error);}
  }

  useEffect(() => {
    const interval = setInterval(() => {
      fetchData(); 
    }, 1000)
    return () => clearInterval(interval)
  }, []);


  useEffect(() => {
    const interval = setInterval(() => {
      if(track=='done'){
        setshowTable(true);
      }
      if(track=='notDone'){
        setshowTable(false);
      }
    }, 10)
    return () => clearInterval(interval)
  }, [track]);



  function handleClickpost () {
  if(window.confirm("Are you sure you want to save this data?")){
    postHeartrate();
    alert("Data saved successfully!");
    fetchHeartrate();
    }
  else{
    console.log("noo")
  }
  }


function handleClickDelete(){
  if(window.confirm("Are you sure you want to delete all your heartbeat history?")){
      window.alert("Your data was deleted successfully.")
  }else{
      console.log("Rejected!!")
  }
}

  function handleClickfetch () {
    fetchHeartrate();
    setTrack("Starting to fetch");
    setTimeout(()=>{
      setTrack('done');
    }, 10)
    setTimeout(()=>{
      scrollWindow();
    }, 100)
  }

  function handleClickClose () {
    setTrack("Starting to fetch");
    setTimeout(()=>{
      setTrack('notDone');
    }, 10)
  }

  function scrollWindow(){
      window.scroll({
        top: 500, // or document.scrollingElement || document.body
        left: 0,        
        behavior: 'auto'      
      });
  }

  function fetchDataClick() {
    handleClickfetch();

  }


  return (
<div>
    <AuthenticatedTemplate>
  <div>
        <div className="homepage">
          <div><Header/></div>
          <div className="video">
          <img
            src="http://127.0.0.1:3001/video"
            alt="Video"
          />
          <div className="glassBox"><Box>
            
          <div className="HRbar">
                 <CircularInput value={value} onChange={setValue}>
                <CircularTrack strokeWidth={5} stroke="#eee" />
                <CircularProgress stroke={`hsl(${value * color}, 100%, 50%)`} />
              </CircularInput>
              </div> 
              <div className="rateinfo">
              <label className="heartrate">{heartRate}</label>
              <label className="shiftLeft">Heart Rate</label>
              </div>
              <button className="butt" onClick={handleClickpost}>Save my Data</button>
            </Box>
            </div>          
        </div>
        {!showtable ? <button  className="fetchdata" onClick={handleClickfetch}>View Your History</button>:null}
        {showtable ? 
        <div className="closeUpdate">
        <button className="blue" onClick={handleClickDelete}>Delete my Data</button> 
        <button className="blue" onClick={handleClickClose}>Close</button>
        <button className="blue" onClick={handleClickfetch}>Update</button>
        </div>
        :<div></div>}
            </div>
          {showtable?
          <div className="hrchart" ref={titleRef}>
            <div className="see">
            <h1 className="heading">Your Heart History </h1>
              {table.map((list)=>{
                return(
                    <div className='bookings-table'>
                      <h1  className='booking-history' style={{
                            textAlign: "left",
                            marginLeft: "5px",
                            marginRight: "7px",
                            fontWeight: "bold",
                            maxWidth: "16.5%",
                            flex: "1.25",
                        }}>Id: {JSON.stringify(list.id)}</h1>
                      <h1 className='booking-history'  style={{
                            textAlign: "left",
                            marginLeft: "60px",
                            marginRight: "20px",
                            fontWeight: "bold",
                            maxWidth: "50%",
                            flex: "1.25",
                        }}>Date: {JSON.stringify(list.date)}</h1>
                      <h1 className='booking-history' style={{
                            textAlign: "left",
                            marginLeft: "50px",
                            marginRight: "16px",
                            fontWeight: "bold",
                          
                            flex: "1.25",
                        }} >Heartbeat: {JSON.stringify(list.heartbeat)}</h1>
                        </div>
                  
                )
              })}
              <div className="linechart">
              <Chart
                title="Heartbeat Trend"
                dataSource={table}
                id="chart"
                
              >

                <ArgumentAxis inverted={true}>
                  <Label customizeText={false} />
                  
                  
                </ArgumentAxis>

                <ValueAxis>
                  <Tick visible={false} />
                  <Label visible={false} />
                </ValueAxis>

                <Series
                  valueField="heartbeat"
                  argumentField="date"
                  type="line"
                  color="#79cac4"
                >
                  <Label visible={true} backgroundColor="#c18e92" />
                </Series>

                <Legend visible={false} />

                <Export enabled={true} />

              </Chart> 
              </div>
            </div>
            </div>
            :
 <div></div>}
            </div>
            </AuthenticatedTemplate>
            <UnauthenticatedTemplate>
            <div>
             <div className="homepage">
              <div><Header/></div>
            <div className="toggle">
            </div>
               <div className="video">
               <img
                 src="http://127.0.0.1:3001/video"
                 alt="Video"
               />
               <div className="glassBox"><Box>
               
               <div className="HRbar">
                 <CircularInput value={value} onChange={setValue}>
                <CircularTrack strokeWidth={5} stroke="#eee" />
                <CircularProgress stroke={`hsl(${value * color}, 100%, 50%)`} />
              </CircularInput>
              </div> 
              <div className="rateinfo">
              <label className="heartrate">{heartRate}</label>
              <label className="shiftLeft">Heart Rate</label>
              </div>
                 </Box>
                 <div className="message">*Please wait 30 sec for calculations</div>
                 </div>
             </div>
                 </div> 
                 </div>  
            </UnauthenticatedTemplate>
            <ScrollButton></ScrollButton>
            </div>       
   );
  };


/*
pageLayout
<AuthenticatedTemplate>
  **code**    
</AuthenticatedTemplate>
      <UnauthenticatedTemplate>
                <h5 className="card-title">Please sign-in to see your profile information.</h5>
            </UnauthenticatedTemplate>
*/
export default App;

