import React, { useEffect, useState } from 'react'
import { Button, Col, Row } from 'react-bootstrap'
import MainLayout from '../layout/MainLayout'
import "../css/page/Top100.css"
import Table from 'react-bootstrap/Table';
import { getBillboardTop100 } from '../api/musicService';
import DatePicker from 'react-datepicker'
import { useNavigate } from 'react-router-dom';
import 'react-datepicker/dist/react-datepicker.css';
const Top100 = () => {
  const [top1001, setTop1001] = useState();
  const [top100, setTop100] = useState();
  const [startDate, setStartDate] = useState(new Date());
  const [dateValue, setDateValue] = useState('')
  const navigate = useNavigate();
  useEffect(()=>{
    dateToString(startDate)
  },[startDate, top100, dateValue,top1001])
  //useEffect 말고 클릭시로 바꿔보자
  let getchartlist = async(e) => {
    e.preventDefault();
    console.log("dateToString",dateValue)
    await getBillboardTop100(dateValue).then((response)=>{
        console.log("response", response.data);
        setTop1001(response.data)
        setTop100(response.data.data);
      }).catch((err)=>{
        console.log("Error", err)
      })
  }

  const dateToString = (date) => {
    let year = date.getFullYear().toString()
    let month = (date.getMonth()+1).toString()
    let day = date.getDate().toString()
    let req_date = year+"-"+month+"-"+day
    setDateValue(req_date)
  }
  const getDayName = (date) => {
    return date.toLocaleDateString('ko-KR', {
      weekday: 'long',
    }).substr(0, 1);
  }
  const createDate = (date) => {
    return new Date(new Date(date.getFullYear()
      , date.getMonth()
      , date.getDate()
      , 0
      , 0
      , 0));
  }
  console.log(top100)
  console.log(top1001)
  return (
    <MainLayout>
        <Row className='top100-title' style={{'marginTop' : '27px'}}>
            <h2>Billboard Hot 100</h2>
            <hr/>
        </Row>
        <Row>
          <Col className='datepicker-wrraper'>
            <DatePicker 
              className='datepicker' 
              selected={startDate} 
              onChange={(date) => {
                setStartDate(date)
              } } 
              dateFormat="yyyy-MM-dd"
              popperPlacement="auto"
              dayClassName={date =>
                getDayName(createDate(date)) === '토' ? "saturday"
              :
                getDayName(createDate(date)) === '일' ? "sunday" : undefined
              }
            />
          </Col>
          <Col>
            <button className='search-btn' onClick={getchartlist}>Search</button>
          </Col>
        </Row>
        <Row>
            <Col xl={10}>
            <Table variant = "dark" striped bordered hover className='top100-table' >
                <thead>
                  <tr>
                    <th>rank</th>
                    <th>title</th>
                    <th>artist</th>
                    <th>diffrent from last week</th>
                  </tr>
                </thead>
                <tbody>
                  {top100 && top100.map((data,index) =>(
                    <tr key={index}>
                      <td>{data.rank}</td>
                      <td>{data.title}</td>
                      <td>{data.artist}</td>
                      <td>{data.diffrent_from_last_week}</td>
                    </tr>
                  ))}
                </tbody>
             </Table>
            </Col>
            <Col>
              <div>

              </div>
            </Col>
        </Row>
    </MainLayout>
  )
}

export default Top100