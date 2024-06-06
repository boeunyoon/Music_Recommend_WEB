import React from 'react'
import { Col, Row } from 'react-bootstrap'
import "../css/layout/MainLayout.css"
import SideBar from '../component/SideBar'
const MainLayout = ({children}, props) => {
  
    console.log("props", props.username)
    console.log(children)
  return (
    <div className='main-layout'>
      <Row>
        <Col lg ="3">
          <div className='profilebox'>
              <SideBar username ={props.username}/>
          </div>
        </Col>
        <Col lg="9">
          <div className='main-component-wrapper'>
            {children}
          </div>
        </Col>
      </Row>
    </div>
  )
}

export default MainLayout