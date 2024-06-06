import React from 'react';
import axios from 'axios';

const getToken=()=>{
    return localStorage.getItem("USER_KEY")
}

export const userLogin=(authRequest)=>{
    console.log('authRequest',authRequest)
    return axios({
        method:'POST',
        url: `${process.env.hostUrl||'http://localhost:8080'}/auth/login`,
        data:authRequest
    })
}

export const fetchUserData=()=>{
    return axios({
        method:'GET',
        url:`${process.env.hostUrl||'http://localhost:8080'}/member/me`,
        headers:{
            'Authorization':'Bearer '+getToken()
        },
    })
}

export const signUp=(authRequest)=>{
    console.log('signup request', authRequest);
    return axios({
        method:'POST',
        url: `${process.env.hostUrl||'http://localhost:8080'}/auth/signup`,
        data:authRequest
    })
}

const calculateRemainingTime = (expirationTime) => {
    const currentTime = new Date().getTime();
    const adjExpirationTime = new Date(expirationTime).getTime();
    const remainingDuration = adjExpirationTime - currentTime;
    return remainingDuration;
  };

export const retrieveStoredToken = () => {
  const storedToken = localStorage.getItem('token');
  const storedExpirationDate = localStorage.getItem('expirationTime') || '0';

  const remaingTime = calculateRemainingTime(+ storedExpirationDate);

  if(remaingTime <= 1000) {
    localStorage.removeItem('token');
    localStorage.removeItem('expirationTime');
    return null
  }

  return {
    token: storedToken,
    duration: remaingTime
  }
}

const createTokenHeader = (token) => {
    return {
      headers: {
        'Authorization': 'Bearer ' + token
      }
    }
}

export const logoutActionHandler = () => {
    localStorage.removeItem('USER_KEY');
};

export const getUserActionHandler = (token) => {
    const response = createTokenHeader(token);
    return axios({
        method:'GET',
        url: `${process.env.hostUrl||'http://localhost:8080'}/member/me`,
        data:response
    });
}
export const getProfileData = () => {
    return axios({
        method:'GET',
        url: `${process.env.hostUrl||'http://localhost:8080'}/profile`,
        headers:{
            'Authorization':'Bearer '+getToken()
        },
    });
}