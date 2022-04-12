# **Software Engineering Group Project: Group 14 - DETECTING HEARTBEAT VIA COLOUR AND/OR MOTION MAGNIFICATION**
**Team Members:** Imogen Green, Utkarsh Gupta, Matthew Grouse, Dishant Tekwani, Max Cunningham, Victoria Fabijaniak, Niall Connolly .
**Demonstrator:** Matt Murtagh.  
**Client:** Serkan Ozkul and Andrew Quirk - Microsoft .

## Build on localhost
1. Clone the repo: 
```
git clone https://github.com/Utkarsh803/Heartbeat_Detection
```

2. Install dependencies
```
npm install
cd client && npm install

May need manual installing:
cd client
npm i devextreme-react
npm i react-circular-input
npm i --save react-signals-plot

Authentication and database required to be set up, but are not required for basic functionality
See here: https://docs.microsoft.com/en-us/azure/active-directory/develop/tutorial-v2-react
https://docs.microsoft.com/en-us/azure/azure-sql/virtual-machines/windows/sql-vm-create-portal-quickstart

```

3. Start the server
```
cd ..
python endPoint.py

cd client
npm start
```

## App Functionality
### Description
This application aims to detect heartbeat via Frontal Face Video and provides accurate results upto 4 BPM* (tested on 8 subjects) in suitable environment and light.

### Video Demonstration:  
https://youtu.be/Tzwx9WraMEw

## Software Engineering Project - Group 15
- Imogen Green (greeni@tcd.ie - 17326096)
- Utkarsh Gupta (guptau@tcd.ie - 19312536)
- Matthew Grouse (grousem@tcd.ie - 19335171)
- Max Cunningham(mcunnin8@tcd.ie - 20333171)
- Niall Connolly(connoln4@tcd.ie - 20332921)
- Victoria Fabijaniak(fabijanw@tcd.ie -20332659)
- Dishant Tekwani(tekwanid@tcd.ie -20309212)

*readings taken after input signal stabilizes