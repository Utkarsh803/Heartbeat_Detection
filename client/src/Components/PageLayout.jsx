import React from "react";
import Navbar from "react-bootstrap/Navbar";
import {useIsAuthenticated } from "@azure/msal-react";
import { SignInButton } from "./SignInButton";

/**
 * Renders the navbar component with a sign-in or sign-out button depending on whether or not a user is authenticated
 * @param props 
 */

export const PageLayout = (props) => {
  const isAuthenticated = useIsAuthenticated();
  return(
    <>
        { isAuthenticated ? <a></a> : <Navbar bg="primary" variant="dark">
        <a className="navbar-brand" href="/">Test</a>
        <SignInButton /> 
       </Navbar> }
      {props.children}
    </>
  );
};