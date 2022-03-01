import React, {Component, useState, useEffect} from "react";
import {useContext} from 'react';
import '../css/Header.css'
import logo from '../assets/mslogo.jpg'



const Header = () => {
    // Sticky Menu Area
    useEffect(() => {
      window.addEventListener("scroll", isSticky);
      return () => {
        window.removeEventListener("scroll", isSticky);
      };
    });
  
    /* Method that will fix header after a specific scrollable */
    const isSticky = (e) => {
      const header = document.querySelector(".header");
      const scrollTop = window.scrollY;
      scrollTop >= 250
        ? header.classList.add("is-sticky")
        : header.classList.remove("is-sticky");
    };


    return (
      <>
        <header className="header">
        <img src={logo}></img>
        <button  className="button">
          Save Data
        </button>
        </header>
      </>
    );
  };
  
  export default Header;