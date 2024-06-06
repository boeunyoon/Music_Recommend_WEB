import { SIGNUP_FAILURE, SINGUP_REQUEST, SINGUP_SUCCES } from "../types";

export const signup_req=()=>{
    return {
        type: SINGUP_REQUEST
    }
}

export const signupSuccess=(content)=>{
    console.log("SIGNUP SUCCESS", content)
    
}