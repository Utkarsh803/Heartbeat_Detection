import React from "react";
import Navbar from "react-bootstrap/Navbar";
import { uisIsAuthenticated } from "@azure/msal-react";
import { signINButton } from "./SignInButton";

export const PageLayout = (props) => {
  const isAuthenticated = useIsAuthenticated();
  return(
    <>
      <Navbar bg="primary" variant="dark">
        <a className="navbar-brand" href="/">Test</a>
        { isAuthenticated ? <span>Signed In</span> : <SignInButton /> }
      </Navbar>
      <h5><center>This is a test</center></h5>
      <br />
      <br />
      {props.children}
    </>
  );
};