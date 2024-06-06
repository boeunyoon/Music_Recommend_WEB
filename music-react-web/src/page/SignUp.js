import React,{useState} from 'react'
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import { signUp } from '../api/authenticationService';
import { useNavigate } from 'react-router-dom';
import '../css/page/SignUp.css'
const SignUp = () => {
    const navigate = useNavigate();
    const [values, setValues] = useState({
      email: '',
      password: '',
      nickname:''
  });
  const handleChange = (e) => {
      e.persist();
      setValues(values => ({
        ...values,
        [e.target.name]: e.target.value
      }));
  }
  const handleSubmit = (e) => {
    e.preventDefault();
    signUp(values).then((response) =>{
        console.log("signup response", response);
        if(response.status == 200){
            navigate("/login");
        }
    }).catch((error)=>{
        console.log("회원가입 실패")
    })
  }
  return (
    <div className='signup-wrapper-final'>
      <div className='signup-wrapper'>
      <h1>Sign Up</h1>
      <Form onSubmit={handleSubmit} noValidate={false} className = 'form-wrapper'>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email" name="email" value={values.email} onChange={handleChange} required/>
        </Form.Group>

        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Nick name</Form.Label>
          <Form.Control type="text" placeholder="Enter Nickname" name="nickname" value={values.nickname} onChange={handleChange} required/>
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
      </Form>
    </div>
    </div>
  )
}

export default SignUp