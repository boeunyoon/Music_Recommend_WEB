import { AUTH_FAILURE, AUTH_REQ, AUTH_SUCCESS } from "./types";

export const authenticate=()=>{
    return {
        type: AUTH_REQ
    }
}

export const authSucces=(content)=>{
    console.log("AUTH SUCCES", content.accessToken)
    localStorage.setItem('USER_KEY', content.accessToken);
    return {
        type : AUTH_SUCCESS,
        payload: content
    }
}

export const authFailure=(error)=>{
    return {
        type: AUTH_FAILURE,
        payload: error
    }
}

