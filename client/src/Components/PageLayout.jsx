import React from "react";
import Navbar from "react-bootstrap/Navbar";
import {useIsAuthenticated } from "@azure/msal-react";
import { SignInButton } from "./SignInButton";
import Header from './Header';
import Box from '@material-ui/core/Box';


/**
 * Renders the navbar component with a sign-in or sign-out button depending on whether or not a user is authenticated
 * @param props 
 */

export const PageLayout = (props) => {
  const isAuthenticated = useIsAuthenticated();
  return(
    <>
   
      {props.children}
    </>
  );
};