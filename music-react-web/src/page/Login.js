import React,{useState} from 'react';
import { connect } from 'react-redux';
import { authFailure, authSucces, authenticate } from '../redux/authAction';
import { userLogin } from '../api/authenticationService';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';
import { Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import '../css/page/Login.css'
import axios from 'axios';

const Login = ({loading, error, ...props}) => {
  const navigate = useNavigate();
  const [values, setValues] = useState({
    email: '',
    password: ''
  });
  console.log(values);

  const handleSubmit=(e)=>{
    e.preventDefault();
    props.authenticate()

    userLogin(values).then((response) => {
      console.log("response", response);
      console.log("token", response.data.accessToken)
      if(response.status == 200){
        authSucces(response.data)
        props.setUser(response.data);
        navigate("/")
      }else{
        props.loginFailure('Something Wrong!Please Try Again'); 
      }
    }).catch((err) => {
      if(err && err.response){
        switch(err.response.status){
          case 401:
            console.log("401 status");
            props.loginFailure("Authentication Failed.Bad Credentials");
            break;
          default:
            props.loginFailure('Something Wrong!Please Try Again');
        }
      }
      else{
        props.loginFailure('Something Wrong!Please Try Again');
      }
    })
  }

  const handleChange = (e) => {
    e.persist();
    setValues(values => ({
      ...values,
      [e.target.name]: e.target.value
    }));
  }

  console.log("Loading ",loading);
  
  return (
    <div className='login-display'>
      <div className='login-wrapper'>
        <h1>Login</h1>
        <Form onSubmit={handleSubmit} noValidate={false} className = 'form-wrapper'>
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control type="email" placeholder="Enter email" name="email" value={values.email} onChange={handleChange} required/>
          </Form.Group>

          <Form.Group className="mb-3" controlId="formBasicPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control type="password" placeholder="Password" value={values.password} onChange={handleChange} name="password" required/>
          </Form.Group>
          <Button variant="primary" type="submit">
            Submit
            {/* {loading && (
                <Spinner
                as="span"
                animation="border"
                size="sm"
                role="status"
                aria-hidden="true"
              />
            )} */}
          </Button>
          <div>
          <a href='/signup'>go to Sign Up</a>
          </div>
        </Form>
        <div className='err-alert' >
          { error &&
            <Alert variant="danger">
              {error}
            </Alert>
          }
        </div>
      </div>
    </div>
  )
}

const mapStateToProps=({auth})=>{
  console.log("state ",auth)
  return {
      loading:auth.loading,
      error:auth.error
}}


const mapDispatchToProps=(dispatch)=>{

  return {
      authenticate :()=> dispatch(authenticate()),
      setUser:(data)=> dispatch(authSucces(data)),
      loginFailure:(message)=>dispatch(authFailure(message))
  }
}
export default connect(mapStateToProps,mapDispatchToProps)(Login);